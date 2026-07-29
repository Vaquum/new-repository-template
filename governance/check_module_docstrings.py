#!/usr/bin/env python3
"""Module-level docstring gate: one line, required on every non-empty module.

Exemptions exist because a docstring can only restate what the reader
already has. In a package built on one public symbol per file with the
filename matching that symbol, the module docstring says what the filename
says -- and the constitution rejects docstrings that restate. Configured
under `module_docstrings` in `.github/gate_config.json`; all exemptions
default off, so this repository is unchanged.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

from _common import (
    REPO_ROOT,
    fail_setup,
    find_python_files,
    gate_config,
    resolve_package_dir,
    significant_lines,
)

BANNER = 'MODULE DOCSTRING GATE'


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


def _public_symbols(tree: ast.Module) -> list[str]:
    """Top-level names a reader would import from this module."""
    names: list[str] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not node.name.startswith('_'):
                names.append(node.name)
    return names


def _is_exempt(path: Path, source: str, config: dict[str, object]) -> bool:
    """Whether this module is exempt from needing a docstring.

    Two independent rules, both off by default:

    `exempt_below_significant_lines` -- a module too small to hold a claim a
    docstring could add. Set to 0 to disable.

    `exempt_filename_matching_single_symbol` -- a module exporting exactly one
    public symbol whose name matches the filename. Here the docstring can only
    repeat the filename, which is the restatement the stance forbids.
    """
    threshold = config.get('exempt_below_significant_lines', 0)
    if isinstance(threshold, int) and not isinstance(threshold, bool) and threshold > 0:
        if significant_lines(path) < threshold:
            return True
    if config.get('exempt_filename_matching_single_symbol') is True:
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return False
        symbols = _public_symbols(tree)
        if len(symbols) == 1 and symbols[0] == path.stem:
            return True
    return False


def _config() -> dict[str, object]:
    """The module_docstrings section, validated. Fails closed on a threshold
    that is not a non-negative integer."""
    cfg = gate_config('module_docstrings', BANNER)
    threshold = cfg.get('exempt_below_significant_lines', 0)
    if isinstance(threshold, bool) or not isinstance(threshold, int) or threshold < 0:
        fail_setup(
            BANNER,
            f'module_docstrings.exempt_below_significant_lines must be a '
            f'non-negative integer, got {threshold!r}',
        )
    excludes = cfg.get('excludes', [])
    if not isinstance(excludes, list) or not all(isinstance(x, str) for x in excludes):
        fail_setup(BANNER, f'module_docstrings.excludes must be a list of strings, got {excludes!r}')
    return cfg


def main() -> int:
    source_dir = resolve_package_dir(BANNER)
    # Read before the scan so an unreadable config blocks on every path.
    config = _config()
    excludes = [*config.get('excludes', []), '__pycache__']
    violations: list[tuple[Path, str]] = []
    for path in find_python_files(source_dir, excludes):
        source = path.read_text(encoding='utf-8')
        if _is_exempt(path, source, config):
            continue
        msg = check_file(path)
        if msg is not None:
            violations.append((path, msg))
    if violations:
        print(f'{BANNER} -- FAIL', file=sys.stderr)
        print('', file=sys.stderr)
        for path, msg in violations:
            rel = path.relative_to(REPO_ROOT)
            print(f'  - {rel}: {msg}', file=sys.stderr)
        print('', file=sys.stderr)
        print(f'{len(violations)} violation(s). Merge blocked.', file=sys.stderr)
        return 1
    print(f'{BANNER} -- PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
