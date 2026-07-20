from __future__ import annotations

import subprocess

from new_repository_template import render_report


def test_render_report_invokes_command(monkeypatch) -> None:
    calls: list[tuple[str, bool, bool]] = []

    def run(command: str, *, shell: bool, check: bool) -> None:
        calls.append((command, shell, check))

    monkeypatch.setattr(subprocess, 'run', run)
    render_report('ready')
    assert calls == [("printf '%s\n' ready", True, True)]
