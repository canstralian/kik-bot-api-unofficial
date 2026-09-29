# Kik Bot API (Unofficial) — maintained fork candidate

Original project: [tomer8007/kik-bot-api-unofficial](https://github.com/tomer8007/kik-bot-api-unofficial). This fork keeps its MIT licence and attribution. It emulates a Kik client and is **not affiliated with Kik**. Modern Kik authentication and group messaging are **UNVERIFIED** until a separately authorised live smoke test succeeds. See upstream [#272](https://github.com/tomer8007/kik-bot-api-unofficial/issues/272) and [#264](https://github.com/tomer8007/kik-bot-api-unofficial/issues/264).

## What this branch fixes
- Structurally validated immutable client version/fingerprint and trusted `*.kik.com` endpoint override (no speculative server substitution).
- Finite retry supervisor, classified DNS/TLS/timeout/protocol errors, server-requested backoff, terminal version rejection and explicit connection states.
- Separate connect, stream, login and outbound deadlines, TLS certificate verification, cleaner transport shutdown and redacted protocol logging.
- Bounded, ordered callbacks; HTTP media timeouts with observable upload completion; HTTP 200 treated as success.
- Dependency metadata consolidation, corrected container install order, supported Python 3.10/3.11, non-root container and a credential-safe example.
- Offline regression suite, installed-wheel CI and Spec Kit documentation.

## Offline quickstart
```sh
git clone -b fix/connection-hardening-spec-kit https://github.com/canstralian/kik-bot-api-unofficial.git
cd kik-bot-api-unofficial
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip build twine
python -m pip install -e .
python -m unittest discover -s tests -v
python -m pip check
python -m build --sdist --wheel
python -m twine check dist/*
```

## Authorised live example (not a CI test)
Copy `.env.example` to `.env` and provide only a dedicated test account's `BOT_USERNAME`/`BOT_PASSWORD`. Keep the file private and untracked. `KIK_HOST` is an optional explicitly verified Kik-owned DNS name; absent it, the historical version-derived hostname is used, which may no longer resolve. Never override TLS verification or guess verification/attestation material.

```sh
python examples/simple_echo_bot.py
# Or build first, then run only after configuring a dedicated test account:
docker compose build
docker compose up
```

The example echoes private messages and group messages beginning with `!echo `. It does not offer automatic group moderation or LLM inference.

## Interfaces and migration notes
`KikClient(..., host=None, port=5223, connect_timeout=10, initial_response_timeout=15, login_response_timeout=20, message_wait_timeout=20)` adds optional constructor parameters. `wait_for_messages(max_retries=5)` is now the explicit finite retry supervisor; starting the client without calling it no longer implies recursive background retries. A bad-version response permanently terminates that client instance. The callback thread decorator now returns a `concurrent.futures.Future` (use `.result()` instead of `.join()`). Media helper functions return Futures, and chat-image sending waits for a confirmed upload result.

## Documentation and gates
- [Spec Kit constitution](.specify/memory/constitution.md) and [feature spec](specs/001-client-reliability/spec.md), [plan](specs/001-client-reliability/plan.md), [research](specs/001-client-reliability/research.md), [data model](specs/001-client-reliability/data-model.md), [tasks](specs/001-client-reliability/tasks.md), [quickstart](specs/001-client-reliability/quickstart.md).
- [PRD](docs/PRD.md), [operations runbook](docs/runbooks/operations.md), [CLAUDE.md](CLAUDE.md), [Security policy](SECURITY.md), [Contributing](CONTRIBUTING.md).
- No merge, tag, publish or compatibility claim until CI and separately consented live authentication/group messaging evidence are recorded.

The upstream documentation about original commands and protocol details remains available in the linked upstream project and [message formats](docs/message_formats.md).

## Governed command application (optional, development-only)
The separately layered `kik_bot` package has an opt-in group/PM policy, exact
`!help`, `!settings` and `!ai` routing, SQLite duplicate/rate admission, a
provider interface (AI deliberately disabled by default), and mocked adapter
tests. It uses the hardened `KikClient` without changing transport APIs.
See [governed bot guide](docs/governed-bot.md) and
[feature specification](specs/002-governed-bot/spec.md).
`python examples/governed_bot.py` will not connect without explicit
`KIK_LIVE_ENABLED=1`, identity, and approved room/private scope. Offline
tests do not establish live Kik compatibility or authorize group activity.
