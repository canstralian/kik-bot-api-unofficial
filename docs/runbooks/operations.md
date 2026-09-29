# Operations runbook: unofficial Kik client

Status: pre-release, live compatibility UNVERIFIED | Scope: authorised test accounts/groups only

## 0. Preconditions and safeguards
Obtain group-owner permission and a dedicated Kik test account. Never use real personal messages in logs/CI. Do not publish .env, credentials, node/device identifiers, password-derived passkeys, challenge responses, attestation tokens or unredacted XMPP. Do not weaken TLS verification or attempt to bypass Kik's verification controls. Current advertised 17.0 profile is historical.

## 1. Local reproducibility
```sh
git switch fix/connection-hardening-spec-kit
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip build twine
python -m pip install -e .
python -m unittest discover -s tests -v
python -m pip check
python -m build --sdist --wheel
python -m twine check dist/*
python -m pip install --force-reinstall --no-deps dist/*.whl
python -c 'import kik_unofficial.client, kik_unofficial.connection_policy; print("wheel import OK")'
```
If dependency resolution fails, record resolver output without credentials. Do not silently expand support beyond CI's Python 3.10/3.11.

## 2. Credential and endpoint preparation
Copy .env.example to .env (git ignored); supply BOT_USERNAME/BOT_PASSWORD only for the dedicated account. Keep KIK_HOST empty unless an independently established Kik-owned endpoint is available; its permitted grammar is *.kik.com, with neither scheme nor path. Empty DEVICE_ID/ANDROID_ID are generated per process; explicitly persisted identifiers must remain private. Never reuse the published demonstration placeholders. Docker uses compose env_file and runs non-root; build with `docker compose build` before attempting `docker compose up`.

## 3. Staged service smoke test (opt-in, after supported client profile is established)
A. Verify DNS resolution for selected host, then verify TLS hostname/certificate without skipping verification.
B. Attempt one connection; record CONNECTING → STREAM_READY (initial stream acknowledgement), not just raw TCP.
C. Verify legitimate authentication response and AUTHENTICATED state. A received login request or TCP socket alone is not success.
D. In an explicitly authorised private test group, issue `!echo test`, confirm one reply; check direct-message echo only with the test account.
E. Stop client permanently and confirm zero further connection attempts, no dangling writer and no sensitive payload in the diagnostic log.
F. Record UTC timestamps, redacted error category, selected version, independently sourced digest provenance and consenting test participants. Do not paste stanzas or tokens.

## 4. Troubleshooting matrix
| Symptom | Meaning | Action |
|---|---|---|
| ValueError on endpoint | Non-Kik host, URL or invalid port | Correct to independently verified Kik-owned DNS name. Never point credentials at arbitrary servers. |
| ValueError on profile | Malformed version or SHA-1 digest | Recheck actual source artifact; do not paste unverified hashes. |
| dns | Name does not resolve | Check configured host and DNS separately; do not assume internet outage. |
| tls | Certificate or TLS handshake failure | Check hostname/system trust and server; never disable verification. |
| timeout | Connect, initial response or login deadline expired | Keep redacted traces, determine which stage; do not claim authenticated. |
| bad_version / TERMINAL | Server explicitly rejected profile | Stop; seek legitimate current-client evidence and update through reviewed PR. |
| server_backoff | Kik requests delay | Wait at least indicated seconds; never shorten or evade controls. |
| retry budget exhausted | Supervisor reached its configured finite budget | Investigate root cause before restarting intentionally. |
| HTTP upload != 200 | Media rejected | Inspect status and retry cap; do not send dependent image message. |
| callback queue saturated | Processing is slower than inbound workload | Restrict bot activity; instrument queue and keep intentional boundedness. |

## 5. Incident and recovery
If diagnostics captured secrets: stop test, restrict artifact/issue access, rotate affected account credentials and invalidate sessions as supported; scrub any public copy according to host policy. If service failures recur: stop supervisor; preserve redacted evidence; do not restart in an uncontrolled loop. If code regression: revert feature PR/commit; verify offline tests, then retest only with approval. Do not backport insecure alternate endpoints or attestation workarounds.

## 6. Merge and release gates
Require PR review, unit and wheel/sdist checks, dependency advisory review, no known secret exposure, compatible client-profile provenance and independently witnessed authorised live login and group roundtrip. Repository-only CI is necessary but not sufficient. Do not tag/publish without a separate explicit release decision.
