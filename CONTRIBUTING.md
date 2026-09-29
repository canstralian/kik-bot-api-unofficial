# Contribution workflow

Target the fork's `new` branch through a feature branch and draft pull request. Read CLAUDE.md and the Spec Kit constitution. Keep changes focused, preserve MIT attribution and provide a spec/task trace for behavioural changes.

Run `python -m unittest discover -s tests -v`, `python -m pip check`, `python -m build --sdist --wheel`, and `python -m twine check dist/*`. Cite actual CI checks rather than asserting them passed. New network paths require mocked positive/negative tests, explicit timeout and fail-closed handling. Never include credentials or personal chat content; avoid live tests in CI.

State user-facing API changes clearly and keep live Kik compatibility a distinct, authorised evidence gate. Do not merge, tag or publish until relevant governance and release conditions are met.
