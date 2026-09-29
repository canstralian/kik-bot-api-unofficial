"""Governed inbound admission -> response -> explicit outbound submission."""

import time
from dataclasses import dataclass
from typing import Callable, Protocol

from .events import IncomingMessage
from .policy import BotPolicy
from .providers import AIProvider, ConversationContext, DisabledAIProvider
from .router import route_message
from .storage import SQLiteSessions


class Publisher(Protocol):
    def send_text(self, jid: str, text: str) -> object:
        ...


@dataclass(frozen=True)
class ProcessingResult:
    status: str
    """Submitted means transport accepted the call, not server delivery."""


class BotRuntime:
    def __init__(self, *, policy: BotPolicy, sessions: SQLiteSessions,
                 publisher: Publisher, provider: AIProvider | None = None,
                 clock: Callable[[], float] = time.time) -> None:
        self.policy = policy
        self.sessions = sessions
        self.publisher = publisher
        self.provider = provider if provider is not None else DisabledAIProvider()
        self.clock = clock

    def handle(self, message: IncomingMessage) -> ProcessingResult:
        if not self.policy.admits(message):
            return ProcessingResult("out_of_scope")
        command = route_message(message.body)
        if command is None:
            return ProcessingResult("ignored")
        admission = self.sessions.admit(
            message, now=self.clock(),
            sender_limit=self.policy.per_sender_minute,
            room_limit=self.policy.per_room_minute,
        )
        if admission.status != "admitted":
            return ProcessingResult(admission.status)

        if command.name == "help":
            reply = "Commands: !help, !settings, !ai <question>."
        elif command.name == "settings":
            ai = "enabled" if self.provider.enabled else "disabled"
            reply = "Group commands are opt-in. AI: " + ai + "."
        elif not command.prompt:
            reply = "Usage: !ai <question>"
        elif not self.provider.enabled:
            reply = "AI is not configured."
        else:
            context = ConversationContext(
                message.room_id, message.sender_id, admission.turns
            )
            try:
                reply = self.provider.generate(command.prompt, context=context)
            except Exception:
                # Do not log provider exception messages: they can contain input.
                return ProcessingResult("provider_error")

        if (not isinstance(reply, str) or not reply.strip()
                or len(reply) > self.policy.max_output_length):
            return ProcessingResult("invalid_reply")
        try:
            self.publisher.send_text(message.room_id, reply)
        except Exception:
            # Already admitted; do not automatically retry an ambiguous send.
            return ProcessingResult("submission_error")
        return ProcessingResult("submitted")
