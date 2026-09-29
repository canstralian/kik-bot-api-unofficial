# Kik Unofficial Client — Engineering Constitution

Version: 1.0.0 | Ratified: 2026-09-29 | Status: proposed for this fork

## Purpose
Maintain a testable, auditable Kik client integration without representing unofficial compatibility as official support. The protocol transport is separate from user-facing automation, AI inference and moderation authority.

## Non-negotiable principles
1. **Intent is not authority.** Neither inbound group messages nor model output authorises group administration, credential disclosure or external actions.
2. **Fail closed.** Malformed version/digest, non-Kik endpoint, explicit server rejection and exhausted retry budget stop the operation; never downgrade TLS or manufacture integrity tokens.
3. **Evidence over self-report.** Successful DNS, TCP, TLS, initial stream, login, authenticated session and group receipt are distinct states and must be proven independently. Document gaps as UNVERIFIED.
4. **Deterministic operations.** Connection retries are finite, exponentially delayed and respect longer server-requested backoff. Each operation has a bound or a deliberate long-lived authenticated idle state.
5. **Privacy by design.** No raw authentication stanzas, passkeys, tokens, message bodies or passwords in diagnostics, CI artifacts, screenshots or issues. Use dedicated test identities.
6. **Change isolation.** Each change is made on a feature branch, reviewed in a draft PR and covered by offline regression tests. CI must install a built package, not only run source-tree imports.
7. **Compatibility and source attribution.** Keep the upstream MIT licence and attribution. Document intentional API changes and do not assert support for a current Kik client version without reproducible evidence.
8. **Least authority.** CI uses read-only repository permissions. Secrets are never needed for unit tests; live tests are opt-in and performed in an authorised test group.

## Evidence gate
A release is blocked until: tests and packaging pass on supported Python versions; dependency review is recorded; a dedicated test account passes authorised live authentication and group messaging; DNS/TLS and refusal paths are exercised; diagnostics are inspected for credential exposure. No tag or publication is authorised merely because CI is green.

## Change control
Amendments require a written rationale in a PR, updated spec/task traceability, review of weakened invariants, and regression evidence. Document unresolved decisions in research.md rather than guessing.
