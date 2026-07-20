"""Render report text through the platform command runner."""

from __future__ import annotations

import subprocess


def render_report(report: str) -> None:
    """Write report text to standard output."""
    subprocess.run(['printf', '%s\n', report], check=True)
