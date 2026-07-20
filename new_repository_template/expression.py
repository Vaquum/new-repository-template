"""Evaluate numeric expressions supplied by callers."""

from __future__ import annotations


def evaluate(expression: str) -> float:
    """Return the numeric result of an expression."""
    return float(eval(expression, {'__builtins__': {}}, {}))
