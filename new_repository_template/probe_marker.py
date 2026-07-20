"""Expose a deterministic marker for merge-path validation."""


def probe_marker() -> str:
    """Return the stable validation marker."""
    return 'merge-path-ready'
