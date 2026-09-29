# Plan — 002

Implement `kik_unofficial/protocol/events.py` as a pure, schema-shaped normalizer using `defusedxml.ElementTree` and standard immutable dataclasses. Use existing JID validators for historical grammar; no account permissions or network calls in this module. Preserve original `kik_unofficial/parser/parser.py` during the fixture-first PR, then wire a validated event bridge in a subsequent change with backward-compatibility tests for callback behaviour.

Place synthetic XML in `tests/fixtures/` and tests in `tests/protocol/` (package marked with __init__.py). Avoid copying original user content from historical docs. Extend CI to validate stacked feature branches without changing release permissions. Publish explicit unknowns in the compatibility matrix.
