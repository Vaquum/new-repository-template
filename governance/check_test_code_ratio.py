#!/usr/bin/env python3
"""Test/code SLOC ratio gate."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Final

REPO_ROOT = Path(__file__).resolve().parents[1]
TYPING_BUDGET = REPO_ROOT / '.github' / 'typing_budget.json'
TEST_DIR = REPO_ROOT / 'tests'

MIN_RATIO: Final[float] = 0.60
MAX_RATIO: Final[float] = 2.00
MIN_SOURCE_SLOC_FOR_GATE: Final[int] = 50


def _package_dir() -> Path:
    # Single source of truth: typing_budget.json's package_root. Fail
    # closed if it cannot be resolved -- a gate that cannot find its scan
    # target blocks the merge instead of passing over an empty tree, so a
    # half-finished package rename cannot silently disable it.
    if not TYPING_BUDGET.is_file():
        print('TEST/CODE RATIO GATE -- FAIL', file=sys.stderr)
        print(f'  missing {TYPING_BUDGET.relative_to(REPO_ROOT)}', file=sys.stderr)
        sys.exit(2)
    data = json.loads(TYPING_BUDGET.read_text(encoding='utf-8'))
    root = data.get('package_root') if isinstance(data, dict) else None
    path = REPO_ROOT / root if isinstance(root, str) and root else None
    if path is None or not path.is_dir():
        print('TEST/CODE RATIO GATE -- FAIL', file=sys.stderr)
        print(f'  package_root {root!r} is not a directory under the repo root', file=sys.stderr)
        sys.exit(2)
    return path


def count_py_sloc(root: Path) -> int:
    if not root.is_dir():
        return 0
    total = 0
    for path in sorted(root.rglob('*.py')):
        for line in path.read_text(encoding='utf-8').splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                total += 1
    return total


def main() -> int:
    source_dir = _package_dir()
    source = count_py_sloc(source_dir)
    test = count_py_sloc(TEST_DIR)
    if source < MIN_SOURCE_SLOC_FOR_GATE:
        # The scan target exists (resolved and checked above); there is
        # just not yet enough source for a ratio to be meaningful.
        print(f'TEST/CODE RATIO GATE -- PASS (source {source} SLOC < {MIN_SOURCE_SLOC_FOR_GATE}, ratio not yet meaningful)')
        return 0
    ratio = test / source if source > 0 else 0.0
    if ratio < MIN_RATIO or ratio > MAX_RATIO:
        print('TEST/CODE RATIO GATE -- FAIL', file=sys.stderr)
        print('', file=sys.stderr)
        print(f'  source SLOC: {source} ({source_dir.name}/)', file=sys.stderr)
        print(f'  test   SLOC: {test} (tests/)', file=sys.stderr)
        print(
            f'  ratio:       {ratio:.2f} '
            f'(required: [{MIN_RATIO:.2f}, {MAX_RATIO:.2f}])',
            file=sys.stderr,
        )
        print('', file=sys.stderr)
        print('Merge blocked.', file=sys.stderr)
        return 1
    print(f'TEST/CODE RATIO GATE -- PASS (source={source}, test={test}, ratio={ratio:.2f})')
    return 0


if __name__ == '__main__':
    sys.exit(main())
