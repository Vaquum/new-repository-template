from __future__ import annotations

from new_repository_template import probe_sequence


def test_probe_sequence_is_ordered() -> None:
    assert probe_sequence() == ('review', 'approval', 'resolution')
