# Product Requirements Document — Governed Kik Client

Owner: canstralian | Status: engineering candidate, not production-ready | Date: 2026-09-29

## Product objective
Restore a reproducible Python transport layer for a command-driven Kik group assistant, separating client interoperability from AI response generation and administrative authority. The deliverable is a maintained unofficial fork, not a replacement for Kik's official client or an attestation bypass.

## Problem
Upstream #272 reports stale client-version rejection and a failed DNS lookup for derived server names. A TCP connection elsewhere did not prove login. Upstream #264 describes possibly changed verification requirements. The old library also had unbounded reconnection, unreliable send waiting, raw payload logging, media success inversion and missing build/CI gates. Evidence: https://github.com/tomer8007/kik-bot-api-unofficial/issues/272 and https://github.com/tomer8007/kik-bot-api-unofficial/issues/264 .

## Users and outcomes
Operator: can identify actionable failure states and stop safely without endless loops. Maintainer: can test errors offline and ship an installable distribution. Group administrator: can add a dedicated opt-in assistant after authorised live verification, with no automatic admin authority or unsolicited messages.

## Scope
Transport/profile configuration and validation; bounded lifecycle and backoff; redaction; deadline-based I/O; bounded callbacks; verified media results; supported Python packaging and container example; automated tests and operational documentation.

## Out of scope
Play Integrity/DeviceCheck/captcha bypass, mass invitations, spam, elevated group actions, automated credentials harvesting, publishing a release before proof, or promising service compatibility from a mocked test.

## Acceptance metrics
100% of defined offline regression scenarios pass in CI on supported Python versions; sdist and wheel pass twine check and wheel import test; missing/invalid credentials fail before operation; bad version causes zero retries; server delay is never shortened; logs contain no authentication payloads; successful live authentication and test-group roundtrip are documented separately before release.

## Milestones and dependencies
M1: repository remediation and documents. M2: CI and dependency advisory review. M3: independently sourced compatible client profile and legitimate verification method. M4: consented integration smoke test. M5: reviewed merge and explicitly authorised release. M3/M4 cannot be completed by source inspection alone.

## Risk register
Service protocol drift: high external dependency, mitigated by explicit compatibility gate. Authentication controls: do not bypass; seek supported operation and document blocker. Privacy: dedicated test account, redacted logs, untracked secrets. Slow callbacks: finite serial queue with observable saturation. Legacy dependency maintenance: package-check plus advisory review. Scope creep: keep LLM integration separate until messaging roundtrip is proven.

## Stakeholder decision
Accepting a green code PR does not authorize tagging, production deployment or a statement that Kik login works. Those require distinct evidence and approval.
