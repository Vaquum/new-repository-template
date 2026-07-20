from __future__ import annotations

import pytest

from new_repository_template import evaluate


@pytest.mark.parametrize(
    ('expression', 'result'),
    [
        ('2 + 3 * 4', 14.0),
        ('(2 + 3) * 4', 20.0),
        ('-2 + +3', 1.0),
    ],
)
def test_evaluate_returns_numeric_result(expression: str, result: float) -> None:
    assert evaluate(expression) == result


def test_evaluate_rejects_non_numeric_constructs() -> None:
    with pytest.raises(ValueError, match='only numeric arithmetic'):
        evaluate('sum([2, 3])')
