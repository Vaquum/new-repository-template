"""The bootstrap file rewrite renames the package but preserves the template slug.

References to the template's own slug (`Vaquum/new-repository-template`) -- the
README provenance link, the SETUP runbook's `--template` command, the label
source -- must survive specialization unchanged, even though every other
occurrence of the seed package name is rewritten.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_template_slug_survives_file_bootstrap(tmp_path: Path) -> None:
    repo = tmp_path / 'repo'
    shutil.copytree(
        REPO_ROOT,
        repo,
        ignore=shutil.ignore_patterns(
            '.git', '.venv', '.venv-lint', '.venv-ruleset', '.venv-ruleset-audit',
            '__pycache__', '.pytest_cache', '.ruff_cache',
        ),
    )
    result = subprocess.run(
        [
            sys.executable, 'governance/bootstrap_repository.py', '--files-only',
            '--repo-name', 'my-new-app', '--owner', 'Vaquum',
        ],
        cwd=repo,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr + result.stdout

    # The rewrite actually ran: the seed package is renamed and gone.
    assert (repo / 'my_new_app').is_dir()
    assert not (repo / 'new_repository_template').exists()
    assert 'new_repository_template' not in (repo / 'pyproject.toml').read_text(encoding='utf-8')

    # ...but references to the template's own slug are preserved verbatim.
    readme = (repo / 'README.md').read_text(encoding='utf-8')
    assert 'https://github.com/Vaquum/new-repository-template' in readme
    setup = (repo / 'SETUP.md').read_text(encoding='utf-8')
    assert '--template Vaquum/new-repository-template' in setup
