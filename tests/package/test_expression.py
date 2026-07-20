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


@pytest.mark.parametrize('expression', ['sum([2, 3])', 'True', '2 +'])
def test_evaluate_rejects_non_numeric_constructs(expression: str) -> None:
    with pytest.raises(ValueError, match='only numeric arithmetic'):
        evaluate(expression)
