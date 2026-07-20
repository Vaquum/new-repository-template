from __future__ import annotations

from pathlib import Path

import pytest

from new_repository_template import load_report


def test_load_report_reads_named_file(tmp_path: Path) -> None:
    (tmp_path / 'daily.txt').write_text('ready', encoding='utf-8')
    assert load_report(tmp_path, 'daily.txt') == 'ready'


def test_load_report_rejects_parent_traversal(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match='escapes storage root'):
        load_report(tmp_path, '../secret.txt')


def test_load_report_rejects_absolute_path(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match='escapes storage root'):
        load_report(tmp_path, '/tmp/secret.txt')
