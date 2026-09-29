# Feature 002: Opt-in governed Kik command application

Base: PR #1 hardening branch. Separate draft PR; no deployment approval.

Acceptance: validated inbound normalization, group allowlist, private-chat
default deny, no admin commands, exact command matching, atomic duplicate
admission and room/sender limits, persistent minimal sessions, provider interface
with disabled default, bounded outbound text, and mocked callback-to-send tests.
No raw stanzas or text in logs or persisted session records.

Negative cases: malformed and oversize messages; unapproved group; self-message;
unknown command; rate saturation; duplicate replay across restarts; provider
failure; invalid output; ambiguous submission failure; concurrent admission.

Deferred gates: third-party AI adapters, receipt validation, independent live
authentication and group-message validation, explicit release authorization.
