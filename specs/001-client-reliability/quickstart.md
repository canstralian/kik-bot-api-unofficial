# Quickstart — offline first

Use Python 3.11 (3.10 is also in CI). This project is an **unofficial** client; current Kik login support is UNVERIFIED. Never run live integration checks with personal credentials or against groups without permission.

```sh
git checkout fix/connection-hardening-spec-kit
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip build twine
python -m pip install -e .
python -m unittest discover -s tests -v
python -m pip check
python -m build --sdist --wheel
python -m twine check dist/*
```

For a locally authorised test only, copy `.env.example` to `.env`; supply BOT_USERNAME and BOT_PASSWORD for a dedicated test account. KIK_HOST is optional and may only contain an independently verified Kik-owned host. Leave DEVICE_ID and ANDROID_ID empty to generate per-process values; set stable values if the test account requires continuity. Never commit the resulting file.

```sh
python examples/simple_echo_bot.py
```

The example responds to direct messages and to group `!echo text` only. It is not an AI bot or proof of modern login compatibility. For a container smoke test, run `docker compose build`; start it only after intentionally configuring the dedicated test account. Follow `docs/runbooks/operations.md` for test evidence and recovery.
