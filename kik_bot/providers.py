"""Model interface: inference can produce text, never messaging authority."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ConversationContext:
    room_id: str
    sender_id: str
    turns: int


class AIProvider(Protocol):
    enabled: bool

    def generate(self, prompt: str, *, context: ConversationContext) -> str:
        """Return bounded text; deployment adapters must enforce own timeout."""
        ...


class ProviderUnavailable(RuntimeError):
    """No inference service has been configured."""


class DisabledAIProvider:
    enabled = False

    def generate(self, prompt: str, *, context: ConversationContext) -> str:
        raise ProviderUnavailable("AI is disabled")
