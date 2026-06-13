#!/usr/bin/env python3
"""Module-level docstring gate: one line, required on every non-empty module."""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TYPING_BUDGET = REPO_ROOT / '.github' / 'typing_budget.json'


def _package_dir() -> Path:
    # Single source of truth: typing_budget.json's package_root. Fail
    # closed if it cannot be resolved -- a gate that cannot find its scan
    # target blocks the merge instead of passing over an empty tree, so a
    # half-finished package rename cannot silently disable it.
    if not TYPING_BUDGET.is_file():
        print('MODULE DOCSTRING GATE -- FAIL', file=sys.stderr)
        print(f'  missing {TYPING_BUDGET.relative_to(REPO_ROOT)}', file=sys.stderr)
        sys.exit(2)
    data = json.loads(TYPING_BUDGET.read_text(encoding='utf-8'))
    root = data.get('package_root') if isinstance(data, dict) else None
    path = REPO_ROOT / root if isinstance(root, str) and root else None
    if path is None or not path.is_dir():
        print('MODULE DOCSTRING GATE -- FAIL', file=sys.stderr)
        print(f'  package_root {root!r} is not a directory under the repo root', file=sys.stderr)
        sys.exit(2)
    return path


def first_statement_docstring(source: str) -> ast.Constant | None:
    # Returns the first-statement docstring node if one exists; else None.
    # Caller is responsible for catching SyntaxError from ast.parse.
    tree = ast.parse(source)
    if not tree.body:
        return None
    first = tree.body[0]
    if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
        return first.value
    return None


def check_file(path: Path) -> str | None:
    # Returns a human-readable violation message, or None on pass.
    source = path.read_text(encoding='utf-8')
    stripped = source.strip()
    if not stripped:
        return None
    try:
        docstring = first_statement_docstring(source)
    except SyntaxError as exc:
        return f'cannot parse as Python (SyntaxError: {exc.msg})'
    if docstring is None:
        return 'first stmt is not a string literal'
    value = docstring.value
    if not isinstance(value, str):
        return 'first stmt is not a string literal'
    if '\n' in value:
        line_count = value.count('\n') + 1
        return f'module docstring spans {line_count} lines'
    return None


def main() -> int:
    source_dir = _package_dir()
    violations: list[tuple[Path, str]] = []
    for path in sorted(source_dir.rglob('*.py')):
        msg = check_file(path)
        if msg is not None:
            violations.append((path, msg))
    if violations:
        print('MODULE DOCSTRING GATE -- FAIL', file=sys.stderr)
        print('', file=sys.stderr)
        for path, msg in violations:
            rel = path.relative_to(REPO_ROOT)
            print(f'  - {rel}: {msg}', file=sys.stderr)
        print('', file=sys.stderr)
        print(f'{len(violations)} violation(s). Merge blocked.', file=sys.stderr)
        return 1
    print('MODULE DOCSTRING GATE -- PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
