from __future__ import annotations

from pathlib import Path

from new_repository_template import load_report


def test_load_report_reads_named_file(tmp_path: Path) -> None:
    (tmp_path / 'daily.txt').write_text('ready', encoding='utf-8')
    assert load_report(tmp_path, 'daily.txt') == 'ready'
