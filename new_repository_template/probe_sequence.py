"""Expose immutable stages for merge-path validation."""


def probe_sequence() -> tuple[str, ...]:
    """Return the ordered validation stages."""
    return ('review', 'approval', 'resolution')
