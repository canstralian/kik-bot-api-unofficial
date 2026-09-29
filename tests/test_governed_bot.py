"""Offline behavior and authority-boundary tests; no network or credentials."""

import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from types import SimpleNamespace

from kik_bot import BotPolicy, BotRuntime, IncomingMessage, SQLiteSessions
from kik_bot.adapter import GovernedBot, KikPublisher
from kik_bot.router import route_message


GROUP = "1100137485028_g@groups.kik.com"
OTHER_GROUP = "1100137485029_g@groups.kik.com"
SENDER = "tester@talk.kik.com"
OTHER = "second@talk.kik.com"
BOT = "botname@talk.kik.com"


class FakePublisher:
    def __init__(self, fail=False):
        self.sent = []
        self.fail = fail

    def send_text(self, jid, text):
        if self.fail:
            raise ConnectionError("synthetic ambiguous send")
        self.sent.append((jid, text))


class FakeAI:
    enabled = True

    def __init__(self, reply="model reply", fail=False):
        self.reply = reply
        self.fail = fail
        self.calls = []

    def generate(self, prompt, *, context):
        self.calls.append((prompt, context))
        if self.fail:
            raise RuntimeError("synthetic private message leak")
        return self.reply


def event(message_id="m1", body="!help", *, sender=SENDER,
          group=GROUP, is_group=True):
    return IncomingMessage(
        message_id, sender, body, group if is_group else sender, is_group
    )


class GovernedRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.db = SQLiteSessions()
        self.publisher = FakePublisher()
        self.now = [1000.]
        self.policy = BotPolicy(
            allowed_group_jids=frozenset({GROUP}), bot_jid=BOT
        )
        self.runtime = BotRuntime(
            policy=self.policy, sessions=self.db, publisher=self.publisher,
            clock=lambda: self.now[0],
        )

    def tearDown(self):
        self.db.close()

    def test_group_is_opt_in_and_noncommands_are_silent(self):
        self.assertEqual(self.runtime.handle(event(group=OTHER_GROUP)).status,
                         "out_of_scope")
        self.assertEqual(self.runtime.handle(event(body="hello")).status, "ignored")
        self.assertEqual(self.publisher.sent, [])

    def test_help_submits_to_group_not_private_sender(self):
        self.assertEqual(self.runtime.handle(event()).status, "submitted")
        self.assertEqual(self.publisher.sent[0][0], GROUP)
        self.assertIn("!ai", self.publisher.sent[0][1])

    def test_private_is_disabled_by_default_and_can_be_enabled(self):
        pm = event(is_group=False)
        self.assertEqual(self.runtime.handle(pm).status, "out_of_scope")
        runtime = BotRuntime(
            policy=BotPolicy(allow_private=True, bot_jid=BOT),
            sessions=self.db, publisher=self.publisher,
            clock=lambda: self.now[0],
        )
        self.assertEqual(runtime.handle(pm).status, "submitted")
        self.assertEqual(self.publisher.sent[-1][0], SENDER)

    def test_self_messages_and_invalid_groups_are_rejected(self):
        self.assertEqual(
            self.runtime.handle(event(sender=BOT)).status, "out_of_scope"
        )
        with self.assertRaises(ValueError):
            BotPolicy(allowed_group_jids=frozenset({"*"}))
        with self.assertRaises(ValueError):
            BotPolicy(bot_jid="unknown")

    def test_ai_defaults_disabled_and_requires_prompt(self):
        self.assertEqual(self.runtime.handle(event(body="!ai why")).status,
                         "submitted")
        self.assertEqual(self.publisher.sent[-1][1], "AI is not configured.")
        self.assertEqual(
            self.runtime.handle(event("m2", "!ai")).status, "submitted"
        )
        self.assertIn("Usage:", self.publisher.sent[-1][1])

    def test_provider_receives_isolated_context_not_raw_stanza(self):
        provider = FakeAI()
        runtime = BotRuntime(
            policy=self.policy, sessions=self.db, publisher=self.publisher,
            provider=provider, clock=lambda: self.now[0],
        )
        self.assertEqual(runtime.handle(event(body="!ai hello")).status,
                         "submitted")
        prompt, context = provider.calls[0]
        self.assertEqual(prompt, "hello")
        self.assertEqual((context.room_id, context.sender_id, context.turns),
                         (GROUP, SENDER, 1))
        self.assertEqual(self.publisher.sent[-1], (GROUP, "model reply"))

    def test_provider_failure_does_not_submit_and_does_not_replay(self):
        runtime = BotRuntime(
            policy=self.policy, sessions=self.db, publisher=self.publisher,
            provider=FakeAI(fail=True),
            clock=lambda: self.now[0],
        )
        self.assertEqual(runtime.handle(event(body="!ai hello")).status,
                         "provider_error")
        self.assertEqual(runtime.handle(event(body="!ai hello")).status,
                         "duplicate")
        self.assertEqual(self.publisher.sent, [])

    def test_invalid_output_and_send_failure_are_not_claimed_delivered(self):
        runtime = BotRuntime(
            policy=self.policy, sessions=self.db, publisher=self.publisher,
            provider=FakeAI(reply="x" * 1001),
            clock=lambda: self.now[0],
        )
        self.assertEqual(runtime.handle(event(body="!ai hello")).status,
                         "invalid_reply")
        bad = BotRuntime(
            policy=self.policy, sessions=self.db, publisher=FakePublisher(fail=True),
            clock=lambda: self.now[0],
        )
        self.assertEqual(bad.handle(event("m2")).status, "submission_error")
        self.assertEqual(bad.handle(event("m2")).status, "duplicate")

    def test_sender_rate_limit_and_room_rate_limit(self):
        self.assertEqual(self.runtime.handle(event("m1")).status, "submitted")
        self.assertEqual(self.runtime.handle(event("m2")).status, "submitted")
        self.assertEqual(self.runtime.handle(event("m3")).status, "submitted")
        self.assertEqual(self.runtime.handle(event("m4")).status, "rate_limited")
        self.assertEqual(self.runtime.handle(event("m4")).status, "duplicate")
        self.now[0] += 61
        self.assertEqual(self.runtime.handle(event("m5")).status, "submitted")
        restricted = BotRuntime(
            policy=BotPolicy(allowed_group_jids=frozenset({GROUP}),
                             per_room_minute=1),
            sessions=SQLiteSessions(), publisher=FakePublisher(),
            clock=lambda: self.now[0],
        )
        try:
            self.assertEqual(restricted.handle(event()).status, "submitted")
            self.assertEqual(
                restricted.handle(event("m2", sender=OTHER)).status,
                "rate_limited",
            )
        finally:
            restricted.sessions.close()

    def test_commands_are_exact_and_settings_read_only(self):
        self.assertIsNone(route_message("some help please"))
        self.assertIsNone(route_message("!help anything"))
        self.assertIsNone(route_message("!admin remove user"))
        self.assertEqual(self.runtime.handle(event(body="!settings")).status,
                         "submitted")
        self.assertIn("disabled", self.publisher.sent[-1][1])

    def test_concurrent_admission_never_exceeds_room_budget(self):
        self.runtime = BotRuntime(
            policy=BotPolicy(allowed_group_jids=frozenset({GROUP}),
                             per_sender_minute=60, per_room_minute=5),
            sessions=self.db, publisher=self.publisher,
            clock=lambda: self.now[0],
        )
        messages = [event(str(i)) for i in range(20)]
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(self.runtime.handle, messages))
        self.assertEqual(sum(r.status == "submitted" for r in results), 5)
        self.assertEqual(len(self.publisher.sent), 5)

    def test_duplicate_and_turn_counter_survive_sqlite_reopen(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bot.sqlite3"
            first = SQLiteSessions(path)
            self.assertEqual(first.admit(event(), now=1000,
                             sender_limit=3, room_limit=20).turns, 1)
            first.close()
            second = SQLiteSessions(path)
            try:
                self.assertEqual(second.admit(event(), now=1001,
                                 sender_limit=3, room_limit=20).status, "duplicate")
                self.assertEqual(second.admit(event("m2"), now=1001,
                                 sender_limit=3, room_limit=20).turns, 2)
            finally:
                second.close()


class AdapterTests(unittest.TestCase):
    def test_kik_adapter_routes_group_and_skips_malformed_input(self):
        db = SQLiteSessions()
        try:
            outgoing = FakePublisher()
            runtime = BotRuntime(
                policy=BotPolicy(allowed_group_jids=frozenset({GROUP})),
                sessions=db, publisher=outgoing,
            )
            callback = GovernedBot(runtime)
            callback.on_group_message_received(SimpleNamespace(
                message_id="a", from_jid=SENDER, group_jid=GROUP, body="!help"
            ))
            callback.on_group_message_received(SimpleNamespace(
                message_id="", from_jid=SENDER, group_jid=GROUP, body="!help"
            ))
            self.assertEqual(len(outgoing.sent), 1)
            self.assertEqual(outgoing.sent[0][0], GROUP)
        finally:
            db.close()

    def test_publisher_uses_existing_client_send_api(self):
        sent = []
        fake_client = SimpleNamespace(
            send_chat_message=lambda jid, text: sent.append((jid, text))
        )
        KikPublisher(fake_client).send_text(GROUP, "ok")
        self.assertEqual(sent, [(GROUP, "ok")])

    def test_invalid_event_shape_fails_closed(self):
        with self.assertRaises(ValueError):
            IncomingMessage("", SENDER, "!help", GROUP, True)
        with self.assertRaises(ValueError):
            IncomingMessage("id", SENDER, None, GROUP, True)
        with self.assertRaises(ValueError):
            IncomingMessage("id", SENDER, "x" * 2001, GROUP, True)


if __name__ == "__main__":
    unittest.main()
