# Compatibility matrix

Date: 2026-09-29. These are deliberately separate evidence categories.

| Layer | Tested scope | Position |
| --- | --- | --- |
| Python runtime | 3.10 / 3.11 | PR #1 CI passed; revalidate downstream PR head |
| Source package and installed wheel | Build, twine check, wheel import outside checkout | PR #1 review repair in CI; check final receipt |
| Docker | Python 3.11 non-root image | PR #1 final-head workflow verifies build |
| Synthetic XML protocol adapter | Direct/group text, typing, receipts, media metadata, status, IQ; negative cases | PR #2 new offline conformance suite, pending final-head CI |
| Historical XMPP stream adapter | Legacy BeautifulSoup code | Exists; not replaced by the new pure normalizer |
| Live endpoint | DNS/TLS at current Kik-owned host | UNVERIFIED |
| Current account login/attestation | Dedicated authorised account | UNVERIFIED; no bypass |
| Group roundtrip | Dedicated permitted test group | UNVERIFIED |
| Governed AI group chatbot | Mocked and live tests | PLANNED; separate application boundary |

Structural client-profile validation proves neither genuine APK provenance nor acceptance by the service. Upstream issue reports are unverified contributor evidence, not an SDK support contract. Block compatibility claims until a redacted, dated live receipt is recorded.
