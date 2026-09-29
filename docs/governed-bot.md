# Governed command bot (stacked on PR #1)

## Architecture and origin
Separately implemented application-level patterns inspired by Pulsebot's router,
response builder and session manager. No Pulsebot source code has been copied;
its root license was not established during source inspection.
`kik_unofficial` remains the transport; `kik_bot` contains opt-in routing, policy,
provider interface, SQLite admission/session ledger, and a callback adapter.
There is no inbound webhook or unauthenticated HTTP endpoint in this increment.

## Offline first
Run `python -m unittest discover -s tests -v` on Python 3.10 or 3.11.
`!help`, `!settings` (read-only), and `!ai <question>` are the only recognised
commands. Normal messages and unknown commands are silent. AI is disabled by
default, and any real provider must be explicitly injected and enforce its own
timeout. Model text does not authorize any account or group administrative action.

## Live configuration (separate authorization and compatibility gate)
Copy `.env.example` to `.env` and use a dedicated bot account. The executable
`python examples/governed_bot.py` fails closed unless `KIK_LIVE_ENABLED=1`,
`BOT_USERNAME`, `BOT_PASSWORD`, and a valid full `BOT_NODE_JID` are supplied,
together with at least one approved `KIK_ALLOWED_GROUP_JIDS` (comma-separated
real group JIDs) or `KIK_PM_ENABLED=1`. Private messages are disabled by default.
`BOT_NODE_JID` is mandatory for the live self-message filter; it is **not** a
verification bypass. `KIK_BOT_DB` defaults to a local SQLite file.
Do not run against a real group until separate consented interoperability
validation establishes login, recipient behavior and delivery receipts.

## Safety and persistence
Admission is scope-first, command-only, then SQLite-atomic duplicate and
per-room/per-sender rate checks (defaults: 20 room and 3 sender commands/minute).
Only IDs, timing, count and scope are retained; message bodies are never
persisted by the application layer. Seen IDs expire after seven days.
Messages reserve their ID before external submission, so ambiguous submission
failures are **not** automatically retried. Status `submitted` reflects only a
returned client send call, not Kik delivery or receipt confirmation.
Malformed events, self-messages, unauthorised groups, ordinary text, duplicate
IDs, over-limit commands and invalid provider outputs do not produce messages.
Public-group sender aliases can change and are never used to infer admin roles.
SQLite provides process-safe admission for multiple workers sharing one DB;
operators must still use a single governed bot transport sender.

## Deferred work
After PR #1 is reviewed/merged and authorised live round-trip evidence exists:
implement provider-specific OpenAI/Dialogflow/local model adapters with explicit
API configuration and deadlines, verified receipt reconciliation, and optional
authenticated FastAPI ingress if actually needed. Do not infer service
compatibility or tag/release from offline tests.
