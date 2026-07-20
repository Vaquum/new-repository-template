"""Evaluate numeric expressions supplied by callers."""

from __future__ import annotations

import ast
import operator
from collections.abc import Callable

BinaryOperator = Callable[[float, float], float]
UnaryOperator = Callable[[float], float]

_BINARY_OPERATORS: dict[type[ast.operator], BinaryOperator] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}
_UNARY_OPERATORS: dict[type[ast.unaryop], UnaryOperator] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _evaluate(node: ast.expr) -> float:
    if isinstance(node, ast.Constant):
        value = node.value
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return float(value)
    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPERATORS:
        operation = _BINARY_OPERATORS[type(node.op)]
        return operation(_evaluate(node.left), _evaluate(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPERATORS:
        operation = _UNARY_OPERATORS[type(node.op)]
        return operation(_evaluate(node.operand))
    raise ValueError('expression must contain only numeric arithmetic')


def evaluate(expression: str) -> float:
    """Return the numeric result of an expression."""
    try:
        parsed = ast.parse(expression, mode='eval')
    except SyntaxError as error:
        raise ValueError('expression must contain only numeric arithmetic') from error
    return _evaluate(parsed.body)
