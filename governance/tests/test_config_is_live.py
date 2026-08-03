"""Every control `governance.yml` declares must actually control something.

The config file is the repository's single answer to "how do I change this".
A key that reads like a control and changes nothing is worse than an absent
one: someone sets it, believes they configured the gate, and the gate carries
on doing what it always did. Three such keys shipped -- `gates.*.enabled`,
`slice.max_closing_references`, `changelog.*` -- and the guard that was
supposed to prevent exactly this covered two of nine sections and matched on
substrings, so it saw none of them.

These tests are the replacement. They assert liveness by *changing* a value
and observing the gate change its verdict, not by grepping for a reader --
a grep is satisfied by a coincidental string literal, which is how the
original guard passed while three controls were dead.
"""
from __future__ import annotations

import ast
import importlib
import json
import shutil
import subprocess
import sys
import types
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG = REPO_ROOT / 'governance.yml'
_IGNORE = shutil.ignore_patterns(
    '.git', '.venv', '.venv-lint', '.venv-ruleset', '.venv-ruleset-audit',
    '__pycache__', 'node_modules', '.pytest_cache', '.ruff_cache', 'htmlcov',
)


def _mod(name: str) -> types.ModuleType:
    return importlib.import_module(name)


def _scratch(tmp_path: Path, mutate: object = None) -> Path:
    """A throwaway copy of the repository, optionally with an edited config."""
    repo = tmp_path / 'repo'
    shutil.copytree(REPO_ROOT, repo, ignore=_IGNORE)
    if callable(mutate):
        data = yaml.safe_load((repo / 'governance.yml').read_text(encoding='utf-8'))
        mutate(data)
        (repo / 'governance.yml').write_text(yaml.safe_dump(data), encoding='utf-8')
    return repo


def _run_gate(repo: Path, script: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(repo / 'governance' / script), *args],
        capture_output=True, text=True, check=False, cwd=repo,
    )


# --- the switch that did nothing ----------------------------------------

def test_disabling_a_gate_disables_it(tmp_path: Path) -> None:
    """`enabled: false` must stop the gate running, not merely be readable."""
    def off(data: dict[str, object]) -> None:
        data['gates']['docstrings']['enabled'] = False  # type: ignore[index]

    repo = _scratch(tmp_path, off)
    result = _run_gate(repo, 'check_docstrings.py')
    assert result.returncode == 0, result.stdout + result.stderr
    assert 'SKIP' in result.stdout, result.stdout


def test_absent_enabled_means_the_gate_runs(tmp_path: Path) -> None:
    """Absent means on: a repository that never mentions the key is governed."""
    def drop(data: dict[str, object]) -> None:
        data['gates']['docstrings'].pop('enabled', None)  # type: ignore[union-attr]

    repo = _scratch(tmp_path, drop)
    result = _run_gate(repo, 'check_docstrings.py')
    assert result.returncode == 0, result.stdout + result.stderr
    assert 'SKIP' not in result.stdout, result.stdout


def test_a_non_boolean_enabled_blocks(tmp_path: Path) -> None:
    """A typo must block rather than silently disable or silently enable."""
    def wrong(data: dict[str, object]) -> None:
        data['gates']['docstrings']['enabled'] = 'no'  # type: ignore[index]

    repo = _scratch(tmp_path, wrong)
    result = _run_gate(repo, 'check_docstrings.py')
    assert result.returncode == 2, result.stdout + result.stderr
    assert 'must be a boolean' in result.stderr


# --- the settings read from the wrong section ---------------------------

def test_max_closing_references_is_honoured() -> None:
    """`slice.max_closing_references` is declared top-level, so read it there."""
    common = _mod('_common')
    declared = yaml.safe_load(CONFIG.read_text(encoding='utf-8'))['slice']
    assert common.section_setting(
        'slice', 'max_closing_references', 99, 'TEST'
    ) == declared['max_closing_references']
    # And the gate reads it from there rather than from `gates.slice`.
    # Matched on the call in the AST, not on the file text: an import line
    # mentioning `section_setting` satisfies a substring check even after the
    # call site has been changed back to the gate reader.
    tree = ast.parse((REPO_ROOT / 'governance' / 'slice_gate.py').read_text(encoding='utf-8'))
    calls = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    assert 'section_setting' in calls, (
        'slice_gate must read max_closing_references from the `slice` section; '
        'reading it through the gate reader looks for `gates.slice`, which the '
        'config does not declare, so the value is silently inert'
    )
    assert 'gate_setting' not in calls


def test_changelog_header_is_honoured() -> None:
    """`changelog.header` likewise: version_gate read `gates.changelog`."""
    common = _mod('_common')
    declared = yaml.safe_load(CONFIG.read_text(encoding='utf-8'))['changelog']
    assert common.section_setting('changelog', 'header', 'WRONG', 'TEST') == declared['header']
    assert common.section_setting('changelog', 'newest', 'WRONG', 'TEST') == declared['newest']


def test_commit_types_come_from_the_config() -> None:
    """`commits.types` was decoration; cc_gate now reads it."""
    cc_gate = _mod('cc_gate')
    declared = set(yaml.safe_load(CONFIG.read_text(encoding='utf-8'))['commits']['types'])
    assert cc_gate.cc_types() == frozenset(declared)


# --- the generic guard, per key rather than per section ------------------

# Keys whose reader is a workflow or an external tool rather than Python.
# Each is named here deliberately so adding one is a visible decision.
_NON_PYTHON_READERS = {
    'repository.name', 'repository.description',
    'runtime.python_version',
    'toolchain.ruff_version', 'toolchain.pyright_version',
    'review.approving_authority',
    'slice.label', 'slice.issue_template',
    'bootstrap.timeout_minutes', 'bootstrap.label_template_repository',
    'bootstrap.secrets', 'bootstrap.variables',
    'ruleset.name',
}


def _all_leaf_keys(data: dict[str, object], prefix: str = '') -> list[str]:
    out: list[str] = []
    for key, value in data.items():
        path = f'{prefix}{key}'
        if isinstance(value, dict) and path != 'gates':
            out.extend(_all_leaf_keys(value, f'{path}.'))
        else:
            out.append(path)
    return out


def test_every_config_key_is_read() -> None:
    """No key in `governance.yml` may be decoration.

    Per key, not per section, and matched against the whole repository rather
    than only `governance/*.py` -- the previous guard was section-level and
    substring-based, which is why `gates.*.enabled`, `slice.max_closing_references`
    and `changelog.*` all sat inert underneath it.
    """
    data = yaml.safe_load(CONFIG.read_text(encoding='utf-8'))
    sources = '\n'.join(
        path.read_text(encoding='utf-8', errors='ignore')
        for pattern in ('governance/*.py', '.github/workflows/*.yml', 'scripts/*.py')
        for path in sorted(REPO_ROOT.glob(pattern))
    )
    orphans: list[str] = []
    for path in _all_leaf_keys({k: v for k, v in data.items() if k != 'schema_version'}):
        leaf = path.rsplit('.', 1)[-1]
        if any(path == e or path.startswith(f'{e}.') for e in _NON_PYTHON_READERS):
            continue
        if f"'{leaf}'" in sources or f'"{leaf}"' in sources or f'{leaf}:' in sources:
            continue
        orphans.append(path)
    assert not orphans, (
        f'governance.yml keys nothing reads: {orphans}. A key that configures '
        f'nothing is worse than an absent one -- someone will set it and believe '
        f'the gate changed. Wire a reader or delete the key.'
    )


def test_every_gate_section_names_a_real_gate() -> None:
    """A `gates.<name>` section must correspond to something that runs."""
    data = yaml.safe_load(CONFIG.read_text(encoding='utf-8'))
    workflows = '\n'.join(
        p.read_text(encoding='utf-8') for p in sorted((REPO_ROOT / '.github/workflows').glob('*.yml'))
    )
    sources = '\n'.join(
        p.read_text(encoding='utf-8') for p in sorted((REPO_ROOT / 'governance').glob('*.py'))
    )
    for name, body in data['gates'].items():
        context = body.get('context')
        known = (
            f"'{name}'" in sources
            or (isinstance(context, str) and context in workflows)
        )
        assert known, f'gates.{name} names no gate that runs'


def test_budgeted_modules_cover_every_governance_module() -> None:
    """Law 6 says every governance module has a line budget. Hold it to that.

    The claim used to name the file-size-balance gate, which never scanned
    `governance/` at all -- so the largest modules in the repository were held
    to shape by nothing.
    """
    budgets = json.loads((REPO_ROOT / '.github/budgets.json').read_text(encoding='utf-8'))
    declared = set(budgets['modules'])
    unbudgeted = sorted(
        f'governance/{path.name}'
        for path in (REPO_ROOT / 'governance').glob('*.py')
        if f'governance/{path.name}' not in declared
    )
    assert not unbudgeted, f'governance modules with no line budget: {unbudgeted}'
