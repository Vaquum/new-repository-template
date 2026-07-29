# Contributing

Read [CLAUDE.md](CLAUDE.md) first. It is the constitution: the laws that block a merge, the workflow, and the code stance. Everything binding is there, and nothing on this page overrides it.

## Local Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Before Opening a PR

Open the PR first, then run the gates locally while CI runs them too — CLAUDE.md's workflow section explains why. Never sit on local verification without an open PR.

The gate suite:

```bash
python -m pytest tests/package -q --maxfail=1
python -m pytest governance/tests -q
python -m ruff check <package> governance tests
python governance/check_module_budgets.py
python governance/check_module_docstrings.py
python governance/check_docstrings.py
```

Every PR bumps `[project].version` and adds a `CHANGELOG.md` entry — the version gate requires both, on every PR, with no exception for docs-only changes.

## What Blocks a Merge

The eleven laws in [CLAUDE.md](CLAUDE.md). A gate failure names its own reason; read the output before changing anything. If the gate is wrong rather than your PR, fix the gate in its own PR — do not work around it.

## Reviewing

The brief every reviewer works from is [`.github/copilot-instructions.md`](.github/copilot-instructions.md). It is the same one GitHub's Copilot review reads, so every reviewer holds one standard.
