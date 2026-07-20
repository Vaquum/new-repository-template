"""Load report content from a configured storage root."""

from __future__ import annotations

from pathlib import Path


def load_report(root: Path, name: str) -> str:
    """Read one UTF-8 report beneath the storage root."""
    storage_root = root.resolve()
    report = (storage_root / name).resolve()
    if not report.is_relative_to(storage_root):
        raise ValueError('report path escapes storage root')
    return report.read_text(encoding='utf-8')
