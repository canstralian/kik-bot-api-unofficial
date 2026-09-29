# Incident response: bot/library

1. Stop the bot/supervisor on credential leakage, unexpected privilege invocation, uncontrolled replies or malformed protocol flood. Freeze outgoing queue; do not replay uncertain sends.
2. Preserve minimum redacted evidence: event IDs (hashed/obfuscated where needed), timestamp, stage, coarse error, CI commit, policy decision and receipt state. Avoid message body/raw XML/captcha/token/identifier disclosure.
3. Rotate exposed secrets/session credentials as service permits, remove leaked artifacts, and review Docker contexts, workflow logs and tracked files.
4. Reproduce with synthetic fixtures and a dedicated group only. Add a regression for the exact trust boundary; do not test against uninvolved users.
5. Restore by reviewed PR and final-head CI, then authorized smoke test, with explicit operator release approval. See SECURITY.md for private disclosure routes.
