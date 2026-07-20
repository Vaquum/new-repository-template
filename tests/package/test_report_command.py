from __future__ import annotations

from new_repository_template import render_report


def test_render_report_writes_stdout(capsys) -> None:
    render_report('ready')
    assert capsys.readouterr().out == 'ready\n'
