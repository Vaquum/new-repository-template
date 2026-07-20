from __future__ import annotations

from new_repository_template import probe_sequence


def test_probe_sequence_is_ordered() -> None:
    sequence = probe_sequence()
    assert isinstance(sequence, tuple)
    assert sequence == ('review', 'approval', 'resolution')
