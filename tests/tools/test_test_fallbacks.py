"""Test fallback gate: try/except in tests is detected; pytest.raises passes."""
from __future__ import annotations

import importlib
import sys
import types
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = REPO_ROOT / 'scripts'


def _load() -> types.ModuleType:
    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))
    return importlib.import_module('check_test_fallbacks')


def test_find_try_statements_flags_try() -> None:
    mod = _load()
    src = 'def test_x() -> None:\n    try:\n        do()\n    except Exception:\n        pass\n'
    assert mod.find_try_statements(src) == [2]


def test_find_try_statements_passes_pytest_raises() -> None:
    mod = _load()
    src = (
        'import pytest\n'
        'def test_x() -> None:\n'
        '    with pytest.raises(ValueError):\n'
        '        do()\n'
    )
    assert mod.find_try_statements(src) == []
