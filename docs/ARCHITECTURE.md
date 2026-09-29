# Architecture: transport separate from intelligence

## Decomposition
1. Kik transport (`kik_unofficial.client`): TLS, auth lifecycle, XMPP transport, bounded reconnect, receipts and outbound transmission.
2. Protocol adapter (`kik_unofficial.protocol`): pure, bounded, namespace-aware normalization. The legacy live stream parser remains separate until a subsequent integration PR.
3. Governed bot runtime (sibling PR #2 introduces `kik_bot` in this fork; proposed future separately deployed `kik-ai-group-bot`): commands, allowlisted conversations, policy, rate limiting, idempotent event ledger and bounded outbox.
4. AI provider adapters (separate app): configurable hosted or local model, no direct authority to perform privileged group actions.
5. State/evidence (separate app): SQLite, per-group settings, redacted diagnostic receipts, bounded history retention.

## Trust boundaries
Network bytes are untrusted. Syntactically valid XML is not authorisation. IQ and receipt payloads only update local state when correlated with a pending, permitted action and matching destination. Provider output is untrusted text and must be checked before publishing. Ordinary conversation requires no bot admin permission. Live authentication remains independently unverified by offline fixture tests.

## Core seams
`normalize_stanza(bytes) -> ProtocolEvent` is deterministic and side-effect free. The future transport-to-event bridge will validate before callback dispatch; the current feature PR does not wire or replace the legacy live parser. The bot runtime will use an injectable transport interface, with a simulated adapter in CI. Outbound messages use a stable local key; only service-side acknowledgements support an observed-delivery state, and exactly-once delivery is not claimed.

## Failure containment
Reject XML DTD/entities, excessive stanza/body sizes, invalid JIDs or message IDs, foreign namespaces, missing group destination, malformed receipts and unexpected event types before application policy. Never log raw packets, private bodies, image URIs, tokens or credentials. On provider errors or policy denial, do not publish a fallback message unless allowed by group settings.

## Release boundaries
Library offline conformance != service compatibility != bot release. See `docs/compatibility-matrix.md`, `specs/005-transport-compatibility/` and `docs/runbooks/operations.md`.
