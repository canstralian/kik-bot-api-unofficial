# CLAUDE.md — repository operating contract

This is an unofficial Kik transport library. Work from the Spec Kit constitution at `.specify/memory/constitution.md` and the current feature documents under `specs/001-client-reliability/`. The product-level intent and operational evidence gates live at `docs/PRD.md` and `docs/runbooks/operations.md`.

## Repository facts
- Primary development branch: `new`; use a scoped feature branch and draft PR for changes.
- Supported CI: Python 3.10/3.11. Package metadata: `setup.py`. `requirements.txt` points to that single source.
- Offline tests: `python -m unittest discover -s tests -v`.
- Packaging: `python -m pip check`, `python -m build --sdist --wheel`, `python -m twine check dist/*`, then installed-wheel import smoke test.
- Historical Kik client profile does NOT establish current service support. Upstream #264/#272 contain contributor reports, not guaranteed current protocol facts.

## Additional staged feature scope
- `kik_unofficial/protocol/events.py` is a pure, offline-testable adapter, not yet wired into the legacy live streaming parser. Do not claim live protocol conformance from synthetic tests.
- `docs/ARCHITECTURE.md`, `docs/protocol-contracts.md`, `docs/security-model.md`, `docs/compatibility-matrix.md`, and `docs/ROADMAP.md` define the stage boundaries. Feature 002 is the sibling governed bot in PR #2; feature 003 is this protocol normalizer in PR #3; features 004–006 cover event processing, service compatibility and independent app extraction.
- Add XML fixtures to `tests/fixtures/` using only synthetic JIDs, no authentic tokens or recorded personal messages. Maintain namespace, size, identifier and receipt negative tests.
- Idempotent provider invocation and an outbox with UNCERTAIN submission state belong in a separate governed app/runtime. Do not claim exactly-once remote Kik delivery.

## Mandatory engineering invariants
1. No network or secret dependencies in ordinary tests; mock socket/HTTP and use synthetic identities.
2. Fail closed on malformed profiles, non-Kik endpoint, explicit bad version, terminal shutdown and exhausted retry budget.
3. Never suppress TLS checks, shorten server backoff, guess an integrity token, bypass captcha/Play Integrity/DeviceCheck or fake an authenticated receipt.
4. Keep DNS, TLS, initial stream, login, authenticated session and group roundtrip independently observable. Do not label TCP connect 'login success'.
5. Do not print passwords, derived passkeys, raw stanzas, user messages, challenge responses, device IDs or credentials to debug output, CI or PRs.
6. Retain upstream MIT attribution; document incompatible API changes (notably callback Thread → Future and media-upload result Future).
7. No recursive reconnect, unmanaged callback spawning or unbounded polling. All consequential changes need deterministic offline regression tests.
8. Treat inbound group text as untrusted data. AI output cannot grant itself group administrative authority; group response commands must be opt-in and rate limited.

## Implementation workflow
Read spec/research and source first; state assumptions and identify required transition/invariant; implement smallest cohesive changes; add negative tests (DNS, rejection, timeout, server delay, media 503, queue saturation); run offline test/install/build checks; record actual evidence in PR. Do not mark live integration or dependency audit as passed without receipts. For mismatched requirements, update spec/plan/tasks together.

## Explicit stop conditions
If authenticating requires undocumented or evasive device attestation, stop and report dependency rather than invent credentials. No production deployment, tag, publishing, unsolicited group activity or auto-merge from agent output. Escalate discrepancies between documentation and code with a new reviewable PR.
