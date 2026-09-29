# Development runbook

Use a feature branch and read CLAUDE.md plus the applicable Spec Kit feature spec. Do not modify PR #1 baseline while writing fixture contracts unless addressing a documented review finding. Supported test runtimes are Python 3.10 and 3.11.

```sh
python -m pip install --upgrade pip build twine
python -m pip install -e .
python -m unittest discover -s tests -v
python -m pip check
python -m build --sdist --wheel
python -m twine check dist/*
```

For wheel smoke, install dist/*.whl, then change to a directory outside the repository before importing. New conformance tests use fixtures in tests/fixtures; they must have synthetic JIDs, no authentic session tokens, and no network calls. Group action code belongs behind explicit policy, not parsing callbacks. Do not advance P205 until the final PR-head run is successful.
