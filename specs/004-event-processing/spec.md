# Feature 004 — Governed event processing (planned)

Requirement: an injectable event consumer persists a unique (conversation_jid, inbound_event_id) record before calling any provider or send action; a transactionally paired outbound intent uses a stable local key. An explicit authorisation matrix enforces group allowlisting, command/mention activation, role checks for privileged operations and bounded user/group rate limits. Reply-to-self and duplicate inbound events must not invoke the provider. Correlate only verified receipts with pending outbound message IDs and correct conversation, actor and receipt type.

State transitions: RECEIVED -> ADMITTED -> GENERATED -> QUEUED -> SUBMITTED -> ACKNOWLEDGED, with DENIED, FAILED and UNCERTAIN branches. Never blindly retry UNCERTAIN remote submissions. The service has no established end-to-end exactly-once guarantee. Accept with deterministic crash/restart, duplicate and missing-receipt tests over SQLite; transport mocked in CI.
