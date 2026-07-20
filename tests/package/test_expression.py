from __future__ import annotations

from new_repository_template import evaluate


def test_evaluate_returns_numeric_result() -> None:
    assert evaluate('2 + 3') == 5.0
