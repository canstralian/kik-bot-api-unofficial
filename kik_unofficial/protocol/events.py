"""Namespace-aware, bounded protocol normalization; never performs an action.

This adapter processes synthetic fixtures or bytes from a *separately verified*
transport. Parsing a stanza does not grant administrative authority or trigger a
reply. Historical XML examples are not evidence of current Kik compatibility.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from xml.etree.ElementTree import Element

from defusedxml import ElementTree as safe_etree

from kik_unofficial.utilities import jid_utilities

MAX_STANZA_BYTES = 65536
MAX_BODY_CHARS = 4096
MAX_RECEIPT_IDS = 64
ID_PATTERN = re.compile(r"[A-Za-z0-9_.:-]{1,128}\Z")
APP_PATTERN = re.compile(r"[A-Za-z0-9_.-]{1,128}\Z")
STANZA_NAMESPACES = ("", "jabber:client", "kik:groups")
RECEIPT_NAMESPACE = "kik:message:receipt"


class ProtocolError(ValueError):
    """A malformed, unsupported or oversized protocol input was rejected."""


class EventKind(str, Enum):
    CHAT = "chat"
    GROUP_CHAT = "group_chat"
    RECEIPT = "receipt"
    TYPING = "typing"
    GROUP_TYPING = "group_typing"
    MEDIA_METADATA = "media_metadata"
    GROUP_STATUS = "group_status"
    IQ_RESPONSE = "iq_response"


@dataclass(frozen=True)
class ProtocolEvent:
    event_id: str
    kind: EventKind
    sender_jid: str | None = None
    recipient_jid: str | None = None
    conversation_jid: str | None = None
    body: str | None = None
    receipt_type: str | None = None
    receipt_ids: tuple[str, ...] = ()
    typing: bool | None = None
    media_app_id: str | None = None
    iq_namespace: str | None = None
    iq_status: str | None = None


def _parts(tag: str) -> tuple[str, str]:
    if tag.startswith("{") and "}" in tag:
        namespace, local = tag[1:].split("}", 1)
        return namespace, local
    return "", tag


def _child(node: Element, name: str, namespaces: tuple[str, ...] = STANZA_NAMESPACES):
    for child in node:
        uri, local = _parts(child.tag)
        if local == name and uri in namespaces:
            return child
    return None


def _identifier(value: str | None, label: str) -> str:
    if not isinstance(value, str) or ID_PATTERN.fullmatch(value) is None:
        raise ProtocolError(f"invalid {label}")
    return value


def _jid(value: str | None, label: str) -> str:
    if not isinstance(value, str) or len(value) > 128 or not jid_utilities.is_valid_jid(value):
        raise ProtocolError(f"invalid {label}")
    return value


def normalize_stanza(data: bytes) -> ProtocolEvent:
    """Normalize a single complete stanza with no network, callbacks or side effects.

    The returned event intentionally excludes raw XML, URLs and tokens. It is
    immutable and requires a separate policy layer before any bot action.
    """
    if not isinstance(data, bytes) or not data or len(data) > MAX_STANZA_BYTES:
        raise ProtocolError("stanza must be 1..65536 bytes")
    try:
        root = safe_etree.fromstring(
            data, forbid_dtd=True, forbid_entities=True, forbid_external=True
        )
    except Exception as exc:
        # Don't reflect potentially sensitive attacker-controlled XML in errors.
        raise ProtocolError("malformed or prohibited XML") from exc

    namespace, root_name = _parts(root.tag)
    if namespace not in STANZA_NAMESPACES or root_name not in ("message", "iq"):
        raise ProtocolError("unsupported stanza root or namespace")

    event_id = _identifier(root.get("id"), "stanza ID")
    if root_name == "iq":
        status = root.get("type")
        if status not in ("result", "error"):
            raise ProtocolError("unsupported IQ status")
        query = _child(root, "query", ("", "jabber:iq:roster", "jabber:iq:register",
                                      "kik:iq:friend", "kik:iq:friend:batch",
                                      "kik:iq:xiphias:bridge", "kik:iq:QoS",
                                      "kik:iq:check-unique", "kik:iq:user-profile",
                                      "kik:iq:convos", "kik:auth:cert"))
        query_namespace = _parts(query.tag)[0] if query is not None else None
        # An IQ result is evidence about the correlated request, never a grant
        # of local permission. Correlation/policy live above this module.
        return ProtocolEvent(event_id, EventKind.IQ_RESPONSE,
                             iq_namespace=query_namespace, iq_status=status)

    sender = _jid(root.get("from"), "sender JID")
    recipient = _jid(root.get("to"), "recipient JID")
    message_type = root.get("type")
    group_node = _child(root, "g")
    group = None
    if group_node is not None:
        group = _jid(group_node.get("jid"), "group JID")
        if not jid_utilities.is_group_jid(group):
            raise ProtocolError("invalid group destination")
    if message_type == "groupchat" and group is None:
        raise ProtocolError("group message missing valid group JID")
    if message_type == "chat" and group is not None:
        raise ProtocolError("direct message carries an unexpected group route")
    if message_type not in ("chat", "groupchat", "receipt", "is-typing"):
        raise ProtocolError("unsupported message type")
    conversation = group or sender

    receipt = _child(root, "receipt", (RECEIPT_NAMESPACE,))
    if message_type == "receipt":
        if receipt is None or receipt.get("type") not in ("delivered", "read"):
            raise ProtocolError("invalid receipt kind or namespace")
        refs = tuple(_identifier(child.get("id"), "receipt message ID")
                     for child in receipt if _parts(child.tag) ==
                     (RECEIPT_NAMESPACE, "msgid"))
        if not 1 <= len(refs) <= MAX_RECEIPT_IDS or len(set(refs)) != len(refs):
            raise ProtocolError("invalid or duplicate receipt reference IDs")
        return ProtocolEvent(event_id, EventKind.RECEIPT, sender, recipient,
                             conversation, receipt_type=receipt.get("type"),
                             receipt_ids=refs)

    typing_node = _child(root, "is-typing")
    if message_type == "is-typing" or typing_node is not None:
        if typing_node is None or typing_node.get("val") not in ("true", "false"):
            raise ProtocolError("invalid typing state")
        kind = EventKind.GROUP_TYPING if group else EventKind.TYPING
        return ProtocolEvent(event_id, kind, sender, recipient, conversation,
                             typing=typing_node.get("val") == "true")

    content = _child(root, "content")
    if content is not None:
        app_id = content.get("app-id")
        if not isinstance(app_id, str) or APP_PATTERN.fullmatch(app_id) is None:
            raise ProtocolError("invalid media application identifier")
        return ProtocolEvent(event_id, EventKind.MEDIA_METADATA, sender,
                             recipient, conversation, media_app_id=app_id)

    if group and (_child(root, "status") is not None or
                  _child(root, "sysmsg", ("", "jabber:client", "kik:msg:info")) is not None):
        return ProtocolEvent(event_id, EventKind.GROUP_STATUS, sender,
                             recipient, conversation)

    body_node = _child(root, "body")
    if body_node is None or body_node.text is None:
        raise ProtocolError("message missing text or supported event marker")
    body = body_node.text
    if not body.strip() or len(body) > MAX_BODY_CHARS:
        raise ProtocolError("invalid message body length")
    kind = EventKind.GROUP_CHAT if group else EventKind.CHAT
    if message_type == "groupchat" and not group:
        raise ProtocolError("group route not validated")
    if message_type == "chat" and group:
        raise ProtocolError("unexpected group route on direct message")
    return ProtocolEvent(event_id, kind, sender, recipient, conversation, body=body)
