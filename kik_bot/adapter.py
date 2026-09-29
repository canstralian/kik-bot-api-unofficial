"""Thin callback adapter for the existing KikClient; no direct API-key webhook."""

from kik_unofficial.callbacks import KikClientCallback

from .events import IncomingMessage
from .runtime import BotRuntime


class KikPublisher:
    def __init__(self, client) -> None:
        self.client = client

    def send_text(self, jid: str, text: str) -> object:
        return self.client.send_chat_message(jid, text)


class GovernedBot(KikClientCallback):
    def __init__(self, runtime: BotRuntime) -> None:
        self.runtime = runtime
        self.client = None

    def _receive(self, message, *, is_group: bool) -> None:
        try:
            event = IncomingMessage.from_kik(message, is_group=is_group)
        except (ValueError, TypeError):
            return  # Malformed input fails closed without raw-stanza logging.
        self.runtime.handle(event)

    def on_chat_message_received(self, message) -> None:
        self._receive(message, is_group=False)

    def on_group_message_received(self, message) -> None:
        self._receive(message, is_group=True)
