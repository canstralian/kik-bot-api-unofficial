# Security model

Assets: bot account, credentials/passkeys, group identity, member messages, media URI tokens, process memory, outbound action permissions and operational audit evidence.

Inputs: untrusted network stanzas, malformed XML, group conversations, chat commands, LLM/provider text and third-party model errors. The protocol adapter parses without I/O, enforces size/DTD/entity/JID restrictions and returns only structured data. A parse result cannot dispatch a message or administer a group.

Authority matrix: ordinary chat reply requires allowed conversation, opt-in command/mention, per-user/group rate budget and accepted policy. Group changes require a separately granted administrative capability, a verified account role and explicit success acknowledgement; these are outside MVP. Neither a model proposal nor a successful IQ status alone grants authority. No bulk group invitation or bypass of identity/attestation protections.

Logging: timestamps, event class and coarse error category only; no bodies, credentials, raw stanzas, full device identifiers, captcha answers, image URLs or session cookies. Secrets enter through untracked .env/environment, never fixtures or CI.

Reliability model: SQLite inbox unique(conversation, message id), one durable outbox item per request, explicit states planned/queued/submitted/acknowledged/uncertain/failed. Ambiguous disconnect after submission is UNCERTAIN; do not blindly resend. The consumer can guarantee local idempotent generation and best-effort delivery, not exactly once at the remote service.

Verification: offline tests for malformed inputs, identity mismatch, duplicate deliveries, denial transitions and confused-deputy attempts; opt-in permitted test-account live checks separately.
