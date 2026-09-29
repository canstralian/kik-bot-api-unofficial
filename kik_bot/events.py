"""Transport-independent, validated inbound message representation."""

from dataclasses import dataclass


@dataclass(frozen=True)
class IncomingMessage:
    message_id: str
    sender_id: str
    body: str
    room_id: str
    is_group: bool

    def __post_init__(self) -> None:
        if not all(
            isinstance(value, str) and value.strip()
            for value in (self.message_id, self.sender_id, self.room_id)
        ):
            raise ValueError("message identifiers must be nonempty strings")
        if not isinstance(self.body, str):
            raise ValueError("message body must be text")
        if len(self.body) > 2000:
            raise ValueError("message body exceeds the fixed admission limit")
        if not isinstance(self.is_group, bool):
            raise ValueError("is_group must be boolean")

    @classmethod
    def from_kik(cls, message, *, is_group: bool) -> "IncomingMessage":
        """Read only parsed fields; never log or propagate the raw stanza."""
        sender = getattr(message, "from_jid", None)
        group = getattr(message, "group_jid", None) if is_group else None
        return cls(
            message_id=getattr(message, "message_id", None),
            sender_id=sender,
            body=getattr(message, "body", None),
            room_id=group if is_group else sender,
            is_group=is_group,
        )
