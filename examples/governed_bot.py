#!/usr/bin/env python3
"""Opt-in Kik command bot. Not a live compatibility or deployment test."""

from kik_unofficial.client import KikClient
from kik_unofficial.configuration import env

from kik_bot.adapter import GovernedBot, KikPublisher
from kik_bot.policy import BotPolicy
from kik_bot.runtime import BotRuntime
from kik_bot.storage import SQLiteSessions


def main() -> None:
    # Running this script is not authority to contact an external service.
    if env.get("KIK_LIVE_ENABLED") != "1":
        raise SystemExit("Live integration disabled; set KIK_LIVE_ENABLED=1 explicitly.")
    username = env.get("BOT_USERNAME")
    password = env.get("BOT_PASSWORD")
    bot_jid = env.get("BOT_NODE_JID")
    if not username or not password or not bot_jid:
        raise SystemExit("BOT_USERNAME, BOT_PASSWORD and BOT_NODE_JID are required.")
    group_jids = frozenset(
        jid.strip() for jid in env.get("KIK_ALLOWED_GROUP_JIDS", "").split(",")
        if jid.strip()
    )
    allow_private = env.get("KIK_PM_ENABLED") == "1"
    if not group_jids and not allow_private:
        raise SystemExit("No approved group or private message scope configured.")
    policy = BotPolicy(
        allowed_group_jids=group_jids, allow_private=allow_private,
        bot_jid=bot_jid,
    )
    sessions = SQLiteSessions(env.get("KIK_BOT_DB") or "bot_sessions.sqlite3")
    publisher = KikPublisher(None)
    callback = GovernedBot(BotRuntime(
        policy=policy, sessions=sessions, publisher=publisher,
    ))
    client = KikClient(
        callback, username, password,
        host=env.get("KIK_HOST") or None,
        device_id=env.get("DEVICE_ID") or None,
        android_id=env.get("ANDROID_ID") or None,
        kik_node=bot_jid,
        enable_console_logging=False,
    )
    publisher.client = client
    try:
        client.wait_for_messages()
    finally:
        sessions.close()


if __name__ == "__main__":
    main()
