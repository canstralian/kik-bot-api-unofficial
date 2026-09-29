"""Explicit operator-granted response scope. Inbound text is not authority."""

from dataclasses import dataclass, field

from kik_unofficial.utilities.jid_utilities import is_group_jid, is_pm_jid


@dataclass(frozen=True)
class BotPolicy:
    allowed_group_jids: frozenset[str] = field(default_factory=frozenset)
    allow_private: bool = False
    bot_jid: str = ""
    per_sender_minute: int = 3
    per_room_minute: int = 20
    max_output_length: int = 1000

    def __post_init__(self) -> None:
        groups = frozenset(self.allowed_group_jids)
        if not all(isinstance(jid, str) and is_group_jid(jid) for jid in groups):
            raise ValueError("every allowed group must have a valid Kik group JID")
        object.__setattr__(self, "allowed_group_jids", groups)
        if not isinstance(self.allow_private, bool):
            raise ValueError("allow_private must be boolean")
        if self.bot_jid and not is_pm_jid(self.bot_jid):
            raise ValueError("bot_jid must be a valid private Kik JID")
        if not 1 <= self.per_sender_minute <= 60:
            raise ValueError("per_sender_minute must be between 1 and 60")
        if not 1 <= self.per_room_minute <= 120:
            raise ValueError("per_room_minute must be between 1 and 120")
        if not 1 <= self.max_output_length <= 2000:
            raise ValueError("max_output_length must be between 1 and 2000")

    def admits(self, message) -> bool:
        if self.bot_jid and message.sender_id == self.bot_jid:
            return False
        if message.is_group:
            return message.room_id in self.allowed_group_jids
        return self.allow_private and message.room_id == message.sender_id
