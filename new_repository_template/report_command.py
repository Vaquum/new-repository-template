"""Render report text through the platform command runner."""

from __future__ import annotations

import sys


def render_report(report: str) -> None:
    """Write report text to standard output."""
    sys.stdout.write(f'{report}\n')
