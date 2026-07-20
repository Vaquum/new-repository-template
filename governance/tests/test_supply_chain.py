"""Supply-chain law: workflow actions are pinned by commit SHA and
checkout credentials are never persisted.

Three assertions over every workflow file, so a regression in any one
of them reds the required tests gate:

  1. Every ``uses:`` reference is pinned to a full 40-hex commit SHA
     with a trailing ``# vX.Y.Z`` comment naming the tag it was
     resolved from. A mutable tag (``@v5``) or branch reference can be
     repointed upstream after review; a commit SHA cannot.
  2. Every ``actions/checkout`` step sets ``persist-credentials:
     false``. The default persists a repo-scoped token into
     ``.git/config`` for every later step in the job; no template
     workflow pushes with that credential (bootstrap pushes through an
     explicit token remote), so nothing may keep it.
  3. Every workflow declares an explicit ``permissions:`` block at the
     workflow or job level, so no job runs on the org default grant.
"""
from __future__ import annotations

import re
from pathlib import Path

from _common import REPO_ROOT

WORKFLOWS_DIR = REPO_ROOT / '.github' / 'workflows'

PINNED_USES_RE = re.compile(r'^\s*(?:- )?uses: \S+@[0-9a-f]{40}\s+# v\d+[\w.-]*$')
ANY_USES_RE = re.compile(r'^\s*(?:- )?uses: ')
CHECKOUT_RE = re.compile(r'^\s*(?:- )?uses: actions/checkout@')


def _workflow_files() -> list[Path]:
    files = sorted(WORKFLOWS_DIR.glob('*.yml'))
    assert files, f'no workflow files found under {WORKFLOWS_DIR}'
    return files


def test_every_action_reference_is_sha_pinned() -> None:
    violations: list[str] = []
    for path in _workflow_files():
        for lineno, line in enumerate(path.read_text(encoding='utf-8').splitlines(), start=1):
            if ANY_USES_RE.match(line) and not PINNED_USES_RE.match(line):
                violations.append(f'{path.name}:{lineno}: {line.strip()}')
    assert not violations, (
        'workflow action references must be pinned to a full commit SHA '
        'with a `# vX.Y.Z` tag comment:\n' + '\n'.join(violations)
    )


def test_every_checkout_disables_credential_persistence() -> None:
    violations: list[str] = []
    for path in _workflow_files():
        lines = path.read_text(encoding='utf-8').splitlines()
        for lineno, line in enumerate(lines, start=1):
            if not CHECKOUT_RE.match(line):
                continue
            window = '\n'.join(lines[lineno - 1:lineno + 6])
            if 'persist-credentials: false' not in window:
                violations.append(f'{path.name}:{lineno}: checkout without persist-credentials: false')
    assert not violations, '\n'.join(violations)


def test_every_workflow_declares_permissions() -> None:
    violations: list[str] = []
    for path in _workflow_files():
        if not re.search(r'^\s*permissions:', path.read_text(encoding='utf-8'), re.MULTILINE):
            violations.append(f'{path.name}: no permissions block at workflow or job level')
    assert not violations, '\n'.join(violations)
