# Implementation tasks and verification ledger — 001

Task status describes repository edits, not a claim that CI or Kik service verification passed.

- [x] T001 Isolate work on fix/connection-hardening-spec-kit; preserve new.
- [x] T002 Validate immutable selected client profile and trusted endpoint.
- [x] T003 Add finite retry supervisor and respect server backoff.
- [x] T004 Add connect/initial-response/login/outbound deadlines and failure categories.
- [x] T005 Keep TLS certificate verification and terminate on bad version.
- [x] T006 Redact transport, message and captcha diagnostic content.
- [x] T007 Bound callbacks and expose completion/failure as Future.
- [x] T008 Correct profile HTTP 200 behaviour; timeout gallery/profile operations; propagate upload failure.
- [x] T009 Correct installation metadata, Docker install ordering, example credentials and configuration precedence.
- [x] T010 Add offline unit tests and CI artifact verification workflow.
- [x] T011 Produce constitution, spec, plan, research, data model, tasks, quickstart, PRD, runbook and CLAUDE.md.
- [x] T012 Baseline at 04f0d69: 17 offline tests per Python version, strict third-party audit, build, wheel and Docker checks passed in Actions run 36548015112. Review remediations after that commit require a new final-head CI receipt before merge.
- [x] T013 Run dependency advisory review and record resolution evidence. Earlier scan identified Pillow 11.3.0 with 35 reported advisory entries; floor raised to 12.3.0, then both Python 3.10/3.11 third-party audits passed at 9e47e968. See Actions run 36547685955.
- [ ] T014 Independently verify current client version, digest and compliant authentication path.
- [ ] T015 Conduct authorised live test: DNS, TLS, stream, authentication, controlled group roundtrip and clean stop.
- [ ] T016 Address independent review findings, validate final-head checks and obtain approval before merge; tag/publish separately only after release gate.

## Traceability
FR-001/002 → connection_policy.py, device_configuration.py → test_connection_policy.py.
FR-003/004/005/006 → client.py → test_client_lifecycle.py.
FR-007 → client.py, parser, xmlns handlers → transport log regression.
FR-008 → threading_utils.py → test_callbacks.py.
FR-009 → profile_pictures.py/content.py → test_uploads.py.
FR-010/011 → setup.py, Dockerfile, examples, CI, operator docs → CI package and workflow receipts.
