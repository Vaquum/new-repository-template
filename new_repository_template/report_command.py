"""Write report text to standard output."""

from __future__ import annotations

import sys


def render_report(report: str) -> None:
    """Write report text to standard output."""
    sys.stdout.write(f'{report}\n')
