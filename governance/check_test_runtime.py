#!/usr/bin/env python3
"""Test-suite runtime gate: the suite completes inside its recorded budget.

CLAUDE.md's stance says a command that runs repeatedly must be profiled and
its profile reported, not merely tolerated. This gate is that stance made
mechanical: the suite writes a runtime profile, and the profile is checked
against a committed ceiling.

The ceiling is per-repository, in `.github/runtime_budget.json`. The template's
own suite is trivial, so its ceiling is loose scaffolding a derived repository
recalibrates against its own observed spread -- the shape of the budget file
records the observation window so a later reader can tell a measured ceiling
from a guessed one.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Final

from _common import REPO_ROOT, fail_setup

BANNER: Final[str] = 'TEST RUNTIME GATE'
BUDGET_PATH: Final[Path] = REPO_ROOT / '.github' / 'runtime_budget.json'


def load_json(path: Path, what: str) -> dict[str, Any]:
    """Read one JSON object, failing closed when it is absent or malformed."""
    if not path.is_file():
        fail_setup(BANNER, f'missing {what}: {path}')
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as exc:
        fail_setup(BANNER, f'cannot read {what} at {path}: {exc}')
    if not isinstance(data, dict):
        fail_setup(BANNER, f'{what} at {path} is not a JSON object')
    return data


def slowest(profile: dict[str, Any], limit: int) -> list[tuple[str, float]]:
    """Return the slowest tests, longest first, capped at limit."""
    raw = profile.get('tests', [])
    if not isinstance(raw, list):
        fail_setup(BANNER, 'profile .tests must be a list')
    rows: list[tuple[str, float]] = []
    for entry in raw:
        if not isinstance(entry, dict):
            continue
        name = str(entry.get('name', '<unnamed>'))
        duration = entry.get('duration', 0.0)
        if isinstance(duration, bool) or not isinstance(duration, (int, float)):
            continue
        rows.append((name, float(duration)))
    return sorted(rows, key=lambda row: -row[1])[:limit]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile', required=True, help='runtime profile JSON')
    parser.add_argument('--enforce', action='store_true',
                        help='exit non-zero when the suite exceeds its ceiling')
    args = parser.parse_args()

    budget = load_json(BUDGET_PATH, 'runtime budget')
    profile = load_json(Path(args.profile), 'runtime profile')

    ceiling = budget.get('max_total_seconds')
    if isinstance(ceiling, bool) or not isinstance(ceiling, (int, float)) or ceiling <= 0:
        fail_setup(BANNER, f'max_total_seconds must be a positive number, got {ceiling!r}')
    limit = budget.get('slowest_tests_limit', 10)
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
        fail_setup(BANNER, f'slowest_tests_limit must be a positive integer, got {limit!r}')

    total = profile.get('total_seconds')
    if isinstance(total, bool) or not isinstance(total, (int, float)):
        fail_setup(BANNER, f'profile .total_seconds must be a number, got {total!r}')

    print(f'suite runtime: {float(total):.2f}s (ceiling {float(ceiling):.2f}s)')
    rows = slowest(profile, limit)
    if rows:
        print(f'slowest {len(rows)}:')
        for name, duration in rows:
            print(f'  {duration:7.2f}s  {name}')

    if float(total) > float(ceiling):
        if not args.enforce:
            print(f'{BANNER} -- PASS (over ceiling, not enforcing)')
            return 0
        print(f'{BANNER} -- FAIL', file=sys.stderr)
        print('', file=sys.stderr)
        print(
            f'  suite took {float(total):.2f}s against a {float(ceiling):.2f}s ceiling.',
            file=sys.stderr,
        )
        print(
            '  Profile the slowest tests above and make them faster; raising the '
            'ceiling is the last resort, not the first.',
            file=sys.stderr,
        )
        print('', file=sys.stderr)
        print('Merge blocked.', file=sys.stderr)
        return 1

    print(f'{BANNER} -- PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
