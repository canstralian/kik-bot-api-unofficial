# Spec Kit-style specification set

This repository maintains a Spec Kit-compatible document arrangement without claiming that the external Spec Kit CLI has been installed or that a template generator was run.

- `memory/constitution.md` contains non-negotiable project principles.
- `../specs/001-client-reliability/spec.md` gives requirements and acceptance criteria.
- `plan.md`, `research.md`, `data-model.md`, `contracts/client-api.md`, `tasks.md` and `quickstart.md` connect implementation to verification.
- `../docs/PRD.md` captures product scope and `../docs/runbooks/operations.md` captures test/deployment gates.
- `../CLAUDE.md` governs agent-assisted changes.

Feature 002 (sibling PR #2): `../specs/002-governed-bot/`. Feature 003: `../specs/003-protocol-conformance/` holds the pure event contract and fixture acceptance ledger. Feature 004: `../specs/004-event-processing/` is planned durable idempotency, authorisation and receipts. Feature 005: `../specs/005-transport-compatibility/` contains the separately gated live service evidence requirements. Feature 006: `../specs/006-ai-bot-extraction/` plans the external governed app. See `../docs/ROADMAP.md`.

Spec changes must keep task and contract references synchronized. Do not mark live Kik tests complete using only mocked CI receipts.
