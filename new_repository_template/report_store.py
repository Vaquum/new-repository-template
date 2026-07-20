"""Load report content from a configured storage root."""

from __future__ import annotations

from pathlib import Path


def load_report(root: Path, name: str) -> str:
    """Read one UTF-8 report beneath the storage root."""
    return (root / name).read_text(encoding='utf-8')
