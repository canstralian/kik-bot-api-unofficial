# Feature 003 — Pure protocol conformance

## User stories
Maintainers can derive deterministic synthetic event records from historical message shapes without a Kik account. Bot builders can use validated, namespace-aware event categories rather than raw packets. Unknown or malformed input cannot produce an outbound action.

## Requirements
FR-201: Parse a bounded, complete stanza using hardened namespace-aware XML parsing; forbid DTD/entity/external content.
FR-202: Validate event, sender, recipient, group and referenced receipt identifiers; enforce expected group route.
FR-203: Normalise direct/group chat, typing, receipts, group status, media metadata and IQ response into immutable structured events.
FR-204: No raw XML, URL or token fields in returned events or parse errors; no implicit authorisation from admin/IQ responses.
FR-205: Supply synthetic fixtures and positive/negative offline regressions without network, credentials or real member messages.
FR-206: Preserve legacy live parser until a separately specified, tested integration replaces it.

## Acceptance
Fixture suite covers direct/group routes, receipt ID correlation inputs, typing both scopes, media metadata without URL, IQ admin response without authority, unsupported types, DTD/entities, oversized data, invalid JIDs and missing group route. CI must execute nested test suite through `unittest discover -s tests`. Mocked tests are not evidence of current Kik server compatibility.
