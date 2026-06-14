#!/usr/bin/env python3
"""Forbid catching any HonestyViolation (or subclass) anywhere under code we own.

AST-based: catches the bare form (`except HonestyViolation`), the dotted
form (`except package.exceptions.HonestyViolation`), and the aliased form
(`from X import HonestyViolation as HV; ...; except HV`). Aliases are
resolved per scope (function / async function / class) via a scope stack
so a function-local rebinding cannot mask another scope's catch -- e.g. a
deliberate `from decimal import Decimal as HonestyViolation` inside one
function does not change how `except HonestyViolation` resolves in a
sibling function. Honesty violations must reach the test boundary;
nothing in production code may swallow them.
"""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TYPING_BUDGET = REPO_ROOT / '.github' / 'typing_budget.json'

HONESTY_EXCEPTIONS = frozenset({
    'HonestyViolation',
    'LookAheadViolation',
    'ConservationViolation',
    'DeterminismViolation',
    'ParityViolation',
    'SanityViolation',
    'PerformanceViolation',
    'StopContractViolation',
})


def _package_dir() -> Path:
    # Single source of truth: typing_budget.json's package_root. Fail
    # closed if it cannot be resolved -- a gate that cannot find its scan
    # target blocks the merge instead of passing over an empty tree, so a
    # half-finished package rename cannot silently disable it.
    if not TYPING_BUDGET.is_file():
        print('NO SWALLOWED VIOLATIONS GATE -- FAIL', file=sys.stderr)
        print(f'  missing {TYPING_BUDGET.relative_to(REPO_ROOT)}', file=sys.stderr)
        sys.exit(2)
    data = json.loads(TYPING_BUDGET.read_text(encoding='utf-8'))
    root = data.get('package_root') if isinstance(data, dict) else None
    path = REPO_ROOT / root if isinstance(root, str) and root else None
    if path is None or not path.is_dir():
        print('NO SWALLOWED VIOLATIONS GATE -- FAIL', file=sys.stderr)
        print(f'  package_root {root!r} is not a directory under the repo root', file=sys.stderr)
        sys.exit(2)
    return path


class _ScopedHandlerWalker(ast.NodeVisitor):
    """Visit imports + except-handlers with a scope stack of alias maps.

    Each stack entry is `(kind, alias_dict)` where `kind` is `'module'`,
    `'function'`, or `'class'`. `_resolve` walks innermost-out and
    SKIPS class scopes -- Python methods do not close over class-body
    bindings as bare names, so a class-body `from X import Y as
    HonestyViolation` does not change how `except HonestyViolation`
    resolves inside a method. Module-level rebinding via plain
    assignment is intentionally NOT followed (adversarial-pattern
    caught at review, not by the gate).
    """

    def __init__(self) -> None:
        self._scopes: list[tuple[str, dict[str, str]]] = [('module', {})]
        self.findings: list[tuple[int, str]] = []

    def _resolve(self, name: str) -> str:
        for kind, scope in reversed(self._scopes):
            if kind == 'class':
                continue
            if name in scope:
                return scope[name]
        return name

    def _record_alias(self, alias_node: ast.alias) -> None:
        local = alias_node.asname or alias_node.name
        self._scopes[-1][1][local] = alias_node.name

    def visit_Import(self, node: ast.Import) -> None:
        for alias_node in node.names:
            self._record_alias(alias_node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        for alias_node in node.names:
            self._record_alias(alias_node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._scopes.append(('function', {}))
        self.generic_visit(node)
        self._scopes.pop()

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._scopes.append(('function', {}))
        self.generic_visit(node)
        self._scopes.pop()

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._scopes.append(('class', {}))
        self.generic_visit(node)
        self._scopes.pop()

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        exc_type = node.type
        if exc_type is not None:
            candidates = exc_type.elts if isinstance(exc_type, ast.Tuple) else [exc_type]
            for c in candidates:
                if isinstance(c, ast.Name):
                    canonical = self._resolve(c.id)
                    if canonical in HONESTY_EXCEPTIONS:
                        self.findings.append((node.lineno, canonical))
                elif isinstance(c, ast.Attribute) and c.attr in HONESTY_EXCEPTIONS:
                    self.findings.append((node.lineno, c.attr))
        self.generic_visit(node)


def check_file(path: Path) -> list[tuple[int, str]]:
    tree = ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    walker = _ScopedHandlerWalker()
    walker.visit(tree)
    return walker.findings


def main() -> int:
    targets = (_package_dir(), REPO_ROOT / 'tests', REPO_ROOT / 'governance' / 'tests')
    all_findings: list[tuple[Path, int, str]] = []
    for target in targets:
        if not target.exists():
            continue
        for py_file in sorted(target.rglob('*.py')):
            for lineno, exc_name in check_file(py_file):
                all_findings.append((py_file.relative_to(REPO_ROOT), lineno, exc_name))
    if all_findings:
        print('NO SWALLOWED VIOLATIONS GATE -- FAIL', file=sys.stderr)
        for path, lineno, exc_name in all_findings:
            print(f'  {path}:{lineno}  caught {exc_name}', file=sys.stderr)
        print(f'\n{len(all_findings)} violation(s). Merge blocked.', file=sys.stderr)
        return 1
    print('NO SWALLOWED VIOLATIONS GATE -- PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
