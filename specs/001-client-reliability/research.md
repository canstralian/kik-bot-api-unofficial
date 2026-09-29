# Research and evidence ledger

## Observed source facts (fork baseline 0136f148)
- Profile default advertised 17.0.0.31357; hostname derived from major/minor version; HOST is module-level.
- A connection thread recursively started another attempt; server backoff was logged as ignored; outbound send waited without terminal check.
- Profile upload treated HTTP 200 as retry/failure and non-200 as success; Docker installed before README was copied; console entry pointed at nonexistent cmdline module.
- There was no tests/ tree or .github/workflows/ in the baseline repository tree.

## External contributor reports — not independently verified
- Upstream #272: version rejection; DNS lookup failed for talk17100an.kik.com; a different hostname permitted TCP but authentication did not complete. https://github.com/tomer8007/kik-bot-api-unofficial/issues/272
- Upstream #264: contributor described additional reCAPTCHA/Play Integrity/DeviceCheck requirements, with later VERIFICATION_FAILED reports. https://github.com/tomer8007/kik-bot-api-unofficial/issues/264

## Validation observations (2026-09-29)
- CI initially passed its regression and wheel checks on both supported Python versions at c3eb8322.
- Adding a strict dependency scan initially failed because the local fork distribution was not published on PyPI. The scan now excludes only the local distribution while auditing installed third-party packages from a frozen requirements snapshot.
- That scan surfaced 35 advisory entries against resolved Pillow 11.3.0. setup.py now requires Pillow >=12.3.0,<13. The subsequent final baseline commit 04f0d69 passed 17 tests per Python version, strict third-party audit, wheel and sdist, installed-wheel smoke tests and Docker image build (Actions run 36548015112). This does not substitute for scanning future locked deployment environments.

## Open unknowns
- Currently supported Kik client profile and genuine APK digest.
- Legitimate device verification mechanism and whether this third-party client can complete it.
- Which Kik-owned endpoint is valid for the authorised test account.
- Compatibility of legacy account/session signing with current service.
- Review remediation on top of passing 04f0d69 requires independent final-head CI and approval; live compatibility remains unverified.

## Evidence policy
Keep offline unit findings distinct from a live service receipt. A DNS result is not a login result. No undocumented guesses, attestation bypasses, fake receipts or secrets in the record.
