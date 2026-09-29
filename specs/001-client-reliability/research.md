# Research and evidence ledger

## Observed source facts (fork baseline 0136f148)
- Profile default advertised 17.0.0.31357; hostname derived from major/minor version; HOST is module-level.
- A connection thread recursively started another attempt; server backoff was logged as ignored; outbound send waited without terminal check.
- Profile upload treated HTTP 200 as retry/failure and non-200 as success; Docker installed before README was copied; console entry pointed at nonexistent cmdline module.
- There was no tests/ tree or .github/workflows/ in the baseline repository tree.

## External contributor reports — not independently verified
- Upstream #272: version rejection; DNS lookup failed for talk17100an.kik.com; a different hostname permitted TCP but authentication did not complete. https://github.com/tomer8007/kik-bot-api-unofficial/issues/272
- Upstream #264: contributor described additional reCAPTCHA/Play Integrity/DeviceCheck requirements, with later VERIFICATION_FAILED reports. https://github.com/tomer8007/kik-bot-api-unofficial/issues/264

## Open unknowns
- Currently supported Kik client profile and genuine APK digest.
- Legitimate device verification mechanism and whether this third-party client can complete it.
- Which Kik-owned endpoint is valid for the authorised test account.
- Compatibility of legacy account/session signing with current service.
- CI dependency advisory outcome and actual test-run results until checks complete.

## Evidence policy
Keep offline unit findings distinct from a live service receipt. A DNS result is not a login result. No undocumented guesses, attestation bypasses, fake receipts or secrets in the record.
