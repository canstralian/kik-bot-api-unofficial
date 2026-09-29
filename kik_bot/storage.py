"""SQLite admission ledger and minimal sessions; no message bodies stored."""

import sqlite3
import threading
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Admission:
    status: str
    turns: int = 0


class SQLiteSessions:
    """Atomic duplicate and two-scope rate checks, safe across callback threads.

    A seen ID is reserved before any outbound effect. Failed sends do not replay
    automatically; operator reconciliation requires an explicit new message.
    """

    def __init__(self, path: str | Path = ":memory:") -> None:
        self._lock = threading.RLock()
        self._db = sqlite3.connect(str(path), timeout=5, check_same_thread=False)
        self._db.execute("PRAGMA busy_timeout=5000")
        self._db.executescript(
            """
            CREATE TABLE IF NOT EXISTS seen (
                room TEXT NOT NULL, sender TEXT NOT NULL,
                message_id TEXT NOT NULL, seen_at REAL NOT NULL,
                PRIMARY KEY (room, sender, message_id)
            );
            CREATE TABLE IF NOT EXISTS rate_events (
                scope TEXT NOT NULL, identity TEXT NOT NULL, at REAL NOT NULL
            );
            CREATE INDEX IF NOT EXISTS rate_lookup
                ON rate_events (scope, identity, at);
            CREATE TABLE IF NOT EXISTS sessions (
                room TEXT NOT NULL, sender TEXT NOT NULL,
                turns INTEGER NOT NULL, last_seen REAL NOT NULL,
                PRIMARY KEY (room, sender)
            );
            """
        )

    def admit(self, message, *, now: float, sender_limit: int,
              room_limit: int) -> Admission:
        sender_key = message.room_id + "\x1f" + message.sender_id
        with self._lock:
            try:
                self._db.execute("BEGIN IMMEDIATE")
                self._db.execute("DELETE FROM rate_events WHERE at < ?", (now - 60,))
                self._db.execute("DELETE FROM seen WHERE seen_at < ?", (now - 604800,))
                duplicate = self._db.execute(
                    "SELECT 1 FROM seen WHERE room=? AND sender=? AND message_id=?",
                    (message.room_id, message.sender_id, message.message_id),
                ).fetchone()
                if duplicate:
                    self._db.commit()
                    return Admission("duplicate")
                self._db.execute(
                    "INSERT INTO seen(room,sender,message_id,seen_at) VALUES(?,?,?,?)",
                    (message.room_id, message.sender_id, message.message_id, now),
                )
                sender_count = self._db.execute(
                    "SELECT COUNT(*) FROM rate_events WHERE scope='sender' "
                    "AND identity=? AND at>?",
                    (sender_key, now - 60),
                ).fetchone()[0]
                room_count = self._db.execute(
                    "SELECT COUNT(*) FROM rate_events WHERE scope='room' "
                    "AND identity=? AND at>?",
                    (message.room_id, now - 60),
                ).fetchone()[0]
                if sender_count >= sender_limit or room_count >= room_limit:
                    self._db.commit()
                    return Admission("rate_limited")
                self._db.executemany(
                    "INSERT INTO rate_events(scope,identity,at) VALUES(?,?,?)",
                    [("sender", sender_key, now), ("room", message.room_id, now)],
                )
                self._db.execute(
                    "INSERT INTO sessions(room,sender,turns,last_seen) VALUES(?,?,1,?) "
                    "ON CONFLICT(room,sender) DO UPDATE SET "
                    "turns=turns+1,last_seen=excluded.last_seen",
                    (message.room_id, message.sender_id, now),
                )
                turns = self._db.execute(
                    "SELECT turns FROM sessions WHERE room=? AND sender=?",
                    (message.room_id, message.sender_id),
                ).fetchone()[0]
                self._db.commit()
                return Admission("admitted", turns)
            except Exception:
                self._db.rollback()
                raise

    def close(self) -> None:
        with self._lock:
            self._db.close()
