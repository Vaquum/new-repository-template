from __future__ import annotations

from new_repository_template import probe_marker


def test_probe_marker_is_stable() -> None:
    assert probe_marker() == 'merge-path-ready'
