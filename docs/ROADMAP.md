# Development tracker — 2026-09-29

This tracker distinguishes implementation, review, merge and live validation. It does not infer a status from a proposed checklist.

| Stage | Deliverable | Status | Evidence/gate |
| --- | --- | --- | --- |
| 0 | Baseline audit | Completed | Fork audit recorded under feature 001 research |
| 1 | Constitution, PRD, Spec Kit, CLAUDE.md, initial runbook | Implemented in PR #1 | Review and merge remain independent |
| 2A | Initial connection, credential and packaging remediation | Implemented in PR #1 | Final-head CI and approval required |
| 2B | Governed command app and SQLite admission | Implemented in sibling draft PR #2 | Independent review, not deployed |
| 3 | Pure protocol normalizer and synthetic conformance fixtures | Implemented in stacked draft PR #3 | Tests and independent review, no live account |
| 4 | Current-service compatibility | Blocked externally | Legitimate verified profile and dedicated account, no verification bypass |
| 5 | Governed AI chatbot | Specified only | Separate app/deployment and simulated transport tests |
| 6 | Release candidate | Not authorised | Library + app CI, security review, documented authorised group roundtrip |

## Work sequence
1. Remediate all actionable PR #1 review findings, run final-head CI, seek independent approval. Do not equate a CodeRabbit COMMENTED review with approval.
2. Complete fixture-first PR #3, then integrate the validator with the stream/event bridge through a later independent PR. Historical documentation examples are sanitized, never reused as real-account fixtures.
3. Implement feature 004 for durable idempotent processing, receipt correlation, governed command routing and controlled retries, first with synthetic failure injection.
4. Document feature 005 external compatibility results distinctly from offline tests. Any service rejection remains a legitimate release blocker.
5. Extract and extend the feature 002 bot under feature 006 as a portable application; target separate repository `canstralian/kik-ai-group-bot` after creation is explicitly supported. Provider integrations must not become dependencies of the transport package.
6. Perform consented dedicated test-group smoke test before any Public Group deployment.

## API and delivery semantics
The local consumer will guarantee one provider invocation per admitted unique inbound event during repeat delivery/restart scenarios through a durable unique key and transactional outbox. Remote delivery remains at-least/at-most ambiguous if a transport fails between submission and acknowledgement. Mark it UNCERTAIN, reconcile by receipt ID or operator action, and never assert exactly-once remote delivery.
