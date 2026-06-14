#!/usr/bin/env python3
"""Diff coverage gate: changed executable lines in the package must be covered."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Final

REPO_ROOT = Path(__file__).resolve().parents[1]
COVERAGE_JSON = REPO_ROOT / 'coverage.json'
TYPING_BUDGET = REPO_ROOT / '.github' / 'typing_budget.json'

# Floor for CHANGED package lines specifically -- higher than the global
# coverage floor, because new code must arrive tested. Raise toward 100 as
# the package matures.
DIFF_FLOOR_PCT: Final[float] = 80.0


def _fail(message: str, *, code: int) -> None:
    print('DIFF COVERAGE GATE -- FAIL', file=sys.stderr)
    print(f'  {message}', file=sys.stderr)
    sys.exit(code)


def parse_added_lines(diff_text: str) -> dict[str, set[int]]:
    """Map each file to the set of new-file line numbers it ADDS.

    Parses `git diff -U0` output: every hunk header `@@ -a,b +c,d @@` resets
    the new-file line counter to c, then each `+` line records and advances it
    while `-` lines (removed) are ignored.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for line in diff_text.splitlines():
        if line.startswith('+++ b/'):
            current = line[len('+++ b/'):]
            added.setdefault(current, set())
        elif line.startswith('@@'):
            plus = line.split('+', 1)[1].split(' ', 1)[0]
            new_line = int(plus.split(',', 1)[0])
        elif current is not None and line.startswith('+') and not line.startswith('+++'):
            added[current].add(new_line)
            new_line += 1
    return {path: lines for path, lines in added.items() if lines}


def evaluate(
    added: dict[str, set[int]],
    files: dict[str, object],
) -> tuple[int, int, list[tuple[str, list[int]]]]:
    """Return (changed_executable, changed_covered, uncovered-by-file)."""
    total = 0
    covered = 0
    uncovered: list[tuple[str, list[int]]] = []
    for rel, lines in added.items():
        info = files.get(rel)
        if not isinstance(info, dict):
            continue
        executed = {int(n) for n in info.get('executed_lines', [])}
        missing = {int(n) for n in info.get('missing_lines', [])}
        executable = lines & (executed | missing)
        if not executable:
            continue
        miss = sorted(lines & missing)
        total += len(executable)
        covered += len(executable) - len(miss)
        if miss:
            uncovered.append((rel, miss))
    return total, covered, uncovered


def _package_root() -> str:
    if not TYPING_BUDGET.is_file():
        _fail(f'missing {TYPING_BUDGET.relative_to(REPO_ROOT)}', code=2)
    data = json.loads(TYPING_BUDGET.read_text(encoding='utf-8'))
    root = data.get('package_root') if isinstance(data, dict) else None
    if not isinstance(root, str) or not root or not (REPO_ROOT / root).is_dir():
        _fail(f'package_root {root!r} is not a directory under the repo root', code=2)
    return str(root)


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[1] != '--base-ref':
        _fail('usage: check_diff_coverage.py --base-ref <ref>', code=2)
    base_ref = sys.argv[2]
    package_root = _package_root()
    if not COVERAGE_JSON.is_file():
        _fail(f'no coverage.json at {COVERAGE_JSON}', code=2)
    result = subprocess.run(
        ['git', 'diff', '-U0', f'{base_ref}...HEAD', '--', package_root],
        check=False, capture_output=True, text=True,
    )
    if result.returncode != 0:
        _fail(f'git diff failed: {result.stderr.strip()}', code=2)
    added = parse_added_lines(result.stdout)
    files = json.loads(COVERAGE_JSON.read_text(encoding='utf-8')).get('files', {})
    total, covered, uncovered = evaluate(added, files)
    if total == 0:
        print('DIFF COVERAGE GATE -- PASS (no changed executable lines in the package)')
        return 0
    pct = 100.0 * covered / total
    if pct < DIFF_FLOOR_PCT:
        print('DIFF COVERAGE GATE -- FAIL', file=sys.stderr)
        print(f'  changed-line coverage {pct:.1f}% (required >= {DIFF_FLOOR_PCT}%)', file=sys.stderr)
        for rel, miss in uncovered:
            preview = ','.join(str(n) for n in miss[:8])
            print(f'    {rel}: uncovered changed lines {preview}', file=sys.stderr)
        print('Merge blocked.', file=sys.stderr)
        return 1
    print(f'DIFF COVERAGE GATE -- PASS (changed-line coverage {pct:.1f}%)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
