#!/usr/bin/env python3
"""Module line-count budget gate."""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BUDGET_PATH = REPO_ROOT / '.github' / 'module_budgets.json'
TYPING_BUDGET = REPO_ROOT / '.github' / 'typing_budget.json'


def count_significant_lines(path: Path) -> int:
    # Budgets are measured against non-blank, non-comment-only lines.
    count = 0
    for line in path.read_text(encoding='utf-8').splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith('#'):
            count += 1
    return count


def _fail_setup(message: str) -> None:
    print('MODULE BUDGET GATE -- FAIL', file=sys.stderr)
    print(f'  {message}', file=sys.stderr)
    sys.exit(2)


def _package_dir() -> Path:
    # Single source of truth: typing_budget.json's package_root. Fail
    # closed if it cannot be resolved -- a gate that cannot find its scan
    # target blocks the merge instead of passing over an empty tree, so a
    # half-finished package rename cannot silently disable it.
    if not TYPING_BUDGET.is_file():
        _fail_setup(f'missing {TYPING_BUDGET.relative_to(REPO_ROOT)} (cannot resolve package_root)')
    data = json.loads(TYPING_BUDGET.read_text(encoding='utf-8'))
    root = data.get('package_root') if isinstance(data, dict) else None
    path = REPO_ROOT / root if isinstance(root, str) and root else None
    if path is None or not path.is_dir():
        _fail_setup(f'package_root {root!r} is not a directory under the repo root')
        raise AssertionError  # unreachable; _fail_setup sys.exits
    return path


def load_budgets() -> dict[str, int]:
    if not BUDGET_PATH.is_file():
        _fail_setup(f'missing budget file: {BUDGET_PATH}')
    try:
        raw = json.loads(BUDGET_PATH.read_text(encoding='utf-8'))
    except (json.JSONDecodeError, OSError) as exc:
        _fail_setup(f'cannot read {BUDGET_PATH}: {exc}')
        raise  # unreachable; _fail_setup sys.exits
    if not isinstance(raw, dict):
        _fail_setup(f'{BUDGET_PATH} is not a JSON object')
    parsed: dict[str, int] = {}
    for key, value in raw.items():
        if not isinstance(value, int) or value <= 0:
            _fail_setup(f'{BUDGET_PATH}["{key}"] must be positive int, got {value!r}')
        parsed[str(key)] = value
    return parsed


def check(budgets: dict[str, int], source_dir: Path) -> tuple[list[tuple[str, int, int]], list[str]]:
    # Returns (over_budget, unbudgeted_source_paths). Any path under the
    # package root that is NOT declared in module_budgets.json is a
    # violation -- otherwise a new module could silently escape the gate.
    over: list[tuple[str, int, int]] = []
    for rel_path, budget in budgets.items():
        path = REPO_ROOT / rel_path
        if not path.is_file():
            continue
        actual = count_significant_lines(path)
        if actual > budget:
            over.append((rel_path, actual, budget))
    package_prefix = f'{source_dir.name}/'
    declared = {key for key in budgets if key.startswith(package_prefix)}
    unbudgeted: list[str] = []
    for path in sorted(source_dir.rglob('*.py')):
        rel = str(path.relative_to(REPO_ROOT))
        if rel not in declared:
            unbudgeted.append(rel)
    return over, unbudgeted


def main() -> int:
    budgets = load_budgets()
    source_dir = _package_dir()
    over, unbudgeted = check(budgets, source_dir)
    if over or unbudgeted:
        print('MODULE BUDGET GATE -- FAIL', file=sys.stderr)
        print('', file=sys.stderr)
        for rel_path, actual, budget in over:
            overage = actual - budget
            print(
                f'  - {rel_path}: {actual} lines '
                f'(budget {budget}, overage +{overage})',
                file=sys.stderr,
            )
        for rel_path in unbudgeted:
            print(
                f'  - {rel_path}: undeclared module; '
                f'add an entry to .github/module_budgets.json',
                file=sys.stderr,
            )
        print('', file=sys.stderr)
        total = len(over) + len(unbudgeted)
        print(f'{total} violation(s). Merge blocked.', file=sys.stderr)
        return 1
    print('MODULE BUDGET GATE -- PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
