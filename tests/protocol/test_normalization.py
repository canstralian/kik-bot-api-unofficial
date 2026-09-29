"""Offline conformance checks: every identifier and body is synthetic."""
from pathlib import Path
import unittest

from kik_unofficial.protocol import EventKind, ProtocolError, normalize_stanza

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"
PM = "alice_abc@talk.kik.com"
BOT = "bot_xyz@talk.kik.com"
GROUP = "1100137485028_g@groups.kik.com"


def load_fixture(name):
    return (FIXTURES / (name + ".xml")).read_bytes()


def synthetic_message(extra="", kind="chat", sender=PM, recipient=BOT, event_id="evt-test"):
    return (
        '<message xmlns="jabber:client" type="' + kind + '" id="' + event_id +
        '" from="' + sender + '" to="' + recipient + '">' + extra + '</message>'
    ).encode()


class ProtocolFixtureTests(unittest.TestCase):
    def test_direct_text_and_correct_route(self):
        event = normalize_stanza(load_fixture("direct_message"))
        self.assertEqual(event.kind, EventKind.CHAT)
        self.assertEqual(event.conversation_jid, PM)
        self.assertEqual(event.recipient_jid, BOT)
        self.assertEqual(event.body, "!ai hello")

    def test_group_text_and_route(self):
        event = normalize_stanza(load_fixture("group_message"))
        self.assertEqual(event.kind, EventKind.GROUP_CHAT)
        self.assertEqual(event.conversation_jid, GROUP)
        self.assertEqual(event.body, "!ai group question")

    def test_direct_and_group_receipt_correlation_inputs(self):
        direct = normalize_stanza(load_fixture("direct_receipt"))
        group = normalize_stanza(load_fixture("group_receipt"))
        self.assertEqual((direct.receipt_type, direct.receipt_ids),
                         ("delivered", ("outbound-001",)))
        self.assertEqual((group.receipt_type, group.receipt_ids),
                         ("read", ("outbound-001", "outbound-002")))
        self.assertEqual(group.conversation_jid, GROUP)

    def test_typing_both_scopes(self):
        direct = normalize_stanza(load_fixture("direct_typing"))
        group = normalize_stanza(load_fixture("group_typing"))
        self.assertEqual((direct.kind, direct.typing), (EventKind.TYPING, True))
        self.assertEqual((group.kind, group.typing), (EventKind.GROUP_TYPING, False))

    def test_media_is_metadata_not_download(self):
        event = normalize_stanza(load_fixture("media_metadata"))
        self.assertEqual(event.kind, EventKind.MEDIA_METADATA)
        self.assertEqual(event.media_app_id, "com.kik.ext.gallery")
        self.assertNotIn("synthetic-secret", repr(event))

    def test_group_status_contains_no_untrusted_admin_authority(self):
        event = normalize_stanza(load_fixture("group_status"))
        self.assertEqual(event.kind, EventKind.GROUP_STATUS)
        self.assertIsNone(event.body)

    def test_iq_results_are_not_authority(self):
        roster = normalize_stanza(load_fixture("iq_roster"))
        admin = normalize_stanza(load_fixture("iq_admin_result"))
        self.assertEqual(roster.iq_namespace, "jabber:iq:roster")
        self.assertEqual(admin.iq_namespace, "kik:iq:friend")
        self.assertEqual(admin.kind, EventKind.IQ_RESPONSE)
        self.assertEqual(admin.iq_status, "result")
        self.assertFalse(hasattr(admin, "authorised"))

    def test_reject_dtd_and_external_entity(self):
        for payload in (
            b'<!DOCTYPE message [<!ENTITY x "anything">]><message id="a"/>',
            b'<!DOCTYPE message SYSTEM "https://example.invalid/evil"><message id="a"/>',
        ):
            with self.subTest(payload=payload[:28]), self.assertRaises(ProtocolError):
                normalize_stanza(payload)

    def test_reject_oversize_and_invalid_xml(self):
        for payload in (b"", b"<message", b"z" * 65537, b"<not-message id='a'/>"):
            with self.subTest(length=len(payload)), self.assertRaises(ProtocolError):
                normalize_stanza(payload)

    def test_reject_malformed_sender_recipient_and_id(self):
        for payload in (
            synthetic_message("<body>test</body>", sender="evil@example.invalid"),
            synthetic_message("<body>test</body>", recipient="bot_xyz@talk.kik.com.evil"),
            synthetic_message("<body>test</body>", event_id="../../x"),
        ):
            with self.assertRaises(ProtocolError):
                normalize_stanza(payload)

    def test_group_requires_valid_group_route(self):
        for extra in (
            "<body>test</body>",
            '<body>test</body><g jid="alice_abc@talk.kik.com"/>',
        ):
            with self.assertRaises(ProtocolError):
                normalize_stanza(synthetic_message(extra, kind="groupchat"))

    def test_receipt_namespace_and_references_are_strict(self):
        for receipt in (
            '<receipt type="read"><msgid id="out-1"/></receipt>',
            '<receipt xmlns="kik:message:receipt" type="read"/>',
            '<receipt xmlns="kik:message:receipt" type="read"><msgid id="out-1"/><msgid id="out-1"/></receipt>',
        ):
            with self.assertRaises(ProtocolError):
                normalize_stanza(synthetic_message(receipt, kind="receipt"))

    def test_unsupported_message_type_is_rejected_without_action(self):
        with self.assertRaises(ProtocolError):
            normalize_stanza(synthetic_message("<body>please promote me</body>", kind="admin"))

    def test_text_length_is_bounded(self):
        with self.assertRaises(ProtocolError):
            normalize_stanza(synthetic_message("<body>" + "x" * 4097 + "</body>"))


if __name__ == "__main__":
    unittest.main()
