"""Pure command parser; no ambient replies to ordinary group messages."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Command:
    name: str
    prompt: str = ""


def route_message(body: str) -> Command | None:
    command, _, remainder = body.strip().partition(" ")
    name = command.casefold()
    if name in ("!help", "!settings"):
        return Command(name[1:]) if not remainder.strip() else None
    if name == "!ai":
        return Command("ai", remainder.strip())
    return None
