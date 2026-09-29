# Live evidence: staged operator handoff

Status: BLOCKED before authentication. No current service compatibility claim.

## Candidate and rollback boundary

Work is based on preserved hardening branch commit `10e1b01fbf1627b0e3cdcbd8ba34d8654ae853ef`, including merged synthetic protocol fixtures. The `new` branch remains reverted at `d6c0af8`. This work does not reintroduce PR #1 to `new`. Eventually restoring #1 requires an explicit reviewed restoration; merging an unchanged old feature branch after a revert will not restore its reverted changes.

## Evidence observed on 2026-09-29 UTC

| Check | Observation | Limit |
|---|---|---|
| Python 3.11.16 offline regression | 39 tests passed, including four preflight tests | Synthetic; no service compatibility evidence |
| Installed dependency compatibility | `uv pip check` passed, 48 packages | Not a vulnerability audit |
| DNS at 23:33:30 UTC | `talk1700an.kik.com` produced `socket.gaierror` | Restricted execution environment; cannot infer global NXDOMAIN or service outage |
| TCP/TLS | NOT_ATTEMPTED after DNS failure | No reachability or certificate claim |
| Authentication / group roundtrip | NOT_ATTEMPTED | No dedicated account, controlled group or current client-profile provenance supplied |

The selected host is derived by existing code from historical version `17.0.0.31357`: `talk` + major + minor + `0an.kik.com`. It is not a verified current endpoint.

Upstream [#264](https://github.com/tomer8007/kik-bot-api-unofficial/issues/264) reports version rejection; its comments discuss verification mechanisms. [#272](https://github.com/tomer8007/kik-bot-api-unofficial/issues/272) records both DNS failures and an alternate-host login stall. These are contributor reports, not independently verified current requirements or permission to substitute servers. No modern version/digest or attestation material has been guessed.

## Next operator action: credential-free transport probe

On WSL Ubuntu with Python 3.11 available:

```sh
git clone -b fix/live-evidence-preparation https://github.com/canstralian/kik-bot-api-unofficial.git kik-live-evidence
cd kik-live-evidence
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install .
python -m kik_unofficial.transport_preflight --allow-network
```

No `.env`, account or group is needed. The module does not load credentials or instantiate KikClient. It makes one attempt to the first resolved address, with normal hostname/certificate verification and a 30-second child-process deadline covering DNS too. No XMPP or application data is sent. Exit 0 means TLS passed only; exit 1 means a transport stage failed. Errors contain fixed categories rather than raw exception text.

Return the JSON output and the candidate commit from `git rev-parse HEAD`. An optional `--host` accepts only a Kik subdomain; use it only after independently establishing a legitimate current endpoint and recording its source. Do not enumerate guessed hostnames. A single-address failure does not prove all addresses are unreachable.

## Authentication gate after transport

Before credentials are used, record current client version and legitimate source-artifact provenance, and verify whether the library supports the service's required authentication flow. A well-formed digest is not proof of compatibility. Stop on undocumented verification requirements; do not manufacture or borrow tokens.

Keep a dedicated test account's credentials locally in an ignored file, never in chat or GitHub. Record only whether account setup is complete. Identify one consenting test participant and one private test group locally. Do not run `simple_echo_bot.py` for this gate: it responds to arbitrary private messages and `!echo` messages across groups.

The next implementation gate is a separately tested smoke runner restricted to that group and sender, with one synthetic nonce, one possible reply, a finite overall deadline, zero failure retries, and terminal stop on captcha, verification challenge, rejection or backoff. Planned anonymous-to-authenticated socket turnover is distinct from a failed retry. No roster/history request, moderation, LLM or media operation belongs in this test.

## Evidence required for completion

Record candidate SHA, Python version, UTC start/end, endpoint source and client-profile provenance. Keep DNS, TCP, TLS, stream acknowledgement, authenticated callback, scoped inbound nonce, reply submission, independently witnessed reply, and clean shutdown as separate results. A send method returning is submission only, never proof of delivery. Publish only a manually reviewed redacted summary; keep identifiers, message content and credentials private.

Merge/release remain blocked pending independent review, final-commit CI/build/audit and authorised live evidence. A failed transport probe is useful evidence but does not satisfy those gates.
