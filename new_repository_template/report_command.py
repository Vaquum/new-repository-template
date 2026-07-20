"""Render report text through the platform command runner."""

from __future__ import annotations

import subprocess


def render_report(report: str) -> None:
    """Write report text to standard output."""
    subprocess.run(f"printf '%s\n' {report}", shell=True, check=True)
