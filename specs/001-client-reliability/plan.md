# Implementation plan — 001

## Architecture
`device_configuration` validates immutable selected version and digest; `connection_policy` defines trusted endpoint policy, connection states and retry delay; `KikClient` supervises a single connection thread at a time; `KikConnection` owns TLS transport, parser and bounded I/O; media upload modules return observable futures. Application callbacks are executed by a bounded serial executor.

## State model
STOPPED → CONNECTING → STREAM_READY → AUTHENTICATING → AUTHENTICATED. Failures can transition to STOPPED/BACKOFF then retry through a finite supervisor. Explicit bad version, permanent shutdown or exhausted retries transition to TERMINAL. TCP/TLS completion is never labelled authenticated.

## Decisions and trade-offs
- Preserve `wait_for_messages(max_retries=5)` as the supervisor entry point; callers relying on automatic reconnection without it must migrate.
- An explicit endpoint override must remain within Kik-owned domain. No probing random hosts and no fallback to third-party routing.
- Keep historical version 17.0 as a shape-validated default rather than assert an unverified newer fingerprint.
- Keep legacy protocol construction in place; avoid guessing current attestation implementation.
- Callback decorator returns a Future rather than an unmanaged Thread. Serial execution preserves submission order but a slow callback can create queue backpressure.
- HTTP media operations expose a Future; image chat submission awaits completed upload, trading latency for correctness.
- Python 3.10/3.11 are the initial supported CI versions. Single-source dependency metadata resides in setup.py until a separate packaging migration.

## Test strategy
Use unittest with mocked sockets, streams, callbacks and HTTP requests. No real Kik traffic in CI. Run installed wheel imports, pip check, sdist/wheel build and twine metadata verification. Log any workflow failure as evidence, not as a bypassable check.

## Live compatibility gate
After offline checks, an authorised operator verifies hostname ownership/resolution, TLS, initial stream, authentication on a dedicated account, inbound/outbound test group delivery and session shutdown. Record exact client version, source of fingerprint, redacted error classification and time. Do not publish tokens, full stanzas or personal chat content.

## Rollout and rollback
Open a draft PR; merge only after tests and review. Release stays separately gated on live compatibility. Roll back to known commit without replacing credentials or disabling server-side protection. Consult operations runbook.
