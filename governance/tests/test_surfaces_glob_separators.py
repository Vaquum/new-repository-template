"""Prove a Surfaces glob means what the issue author reads it to mean.

`fnmatch` does not treat `/` as a separator, so `governance/*` covered the
whole subtree beneath it while rule 7 still reported PASS. The scope contract
is the only thing standing between a slice and an unrelated file, so the
interesting cases here are the ones that must NOT match.
"""
from __future__ import annotations

import pytest
from slice_gate import path_matches


@pytest.mark.parametrize(
    ('path', 'glob'),
    [
        ('governance/slice_gate.py', 'governance/*'),
        ('governance/slice_gate.py', 'governance/*.py'),
        ('governance/slice_gate.py', 'governance/slice_gate.py'),
        ('CHANGELOG.md', '*.md'),
        ('CHANGELOG.md', '*'),
        ('governance/tests/test_x.py', 'governance/**'),
        ('governance/tests/test_x.py', 'governance/**/*.py'),
        # `**/` matches zero directories too.
        ('x.py', '**/x.py'),
        ('a/b/x.py', '**/x.py'),
        ('governance/slice_gate.py', 'governance/slice_?ate.py'),
    ],
)
def test_paths_their_glob_covers(path: str, glob: str) -> None:
    assert path_matches(path, glob)


@pytest.mark.parametrize(
    ('path', 'glob'),
    [
        # The defect: a single star must not cross a separator.
        ('governance/tests/deep.py', 'governance/*'),
        ('governance/tests/deep.py', 'governance/*.py'),
        ('docs/Developer/Configuration.md', 'docs/*'),
        ('governance/slice_gate.py', '*'),
        ('governance/slice_gate.py', '*.py'),
        ('a/b/c.md', '*.md'),
        # `?` is one character, and never the separator.
        ('governance/x/ate.py', 'governance/slice_?ate.py'),
        ('a/b.py', 'a?b.py'),
        # A different subtree entirely.
        ('tests/package/test_x.py', 'governance/**'),
        ('governance.yml', 'governance/**'),
    ],
)
def test_paths_their_glob_must_not_cover(path: str, glob: str) -> None:
    assert not path_matches(path, glob)


def test_a_glob_is_anchored_at_both_ends() -> None:
    """A partial match must not count, or `governance/x.py` would be
    covered by `governance/x` and by `overnance/x.py` alike."""
    assert not path_matches('governance/slice_gate.py', 'governance/slice_gate')
    assert not path_matches('governance/slice_gate.py', 'slice_gate.py')
    assert not path_matches('agovernance/slice_gate.py', 'governance/*.py')


def test_regex_metacharacters_in_a_path_are_literal() -> None:
    """A dot is a dot. Under a naive translation `a.py` would match `axpy`."""
    assert path_matches('a.py', 'a.py')
    assert not path_matches('axpy', 'a.py')
    assert not path_matches('docs/a+b.md', 'docs/a+.md')
    assert path_matches('docs/a+b.md', 'docs/a+b.md')


def test_the_double_star_that_still_covers_everything() -> None:
    """`**` is genuinely universal, which is why the vacuous-glob guard
    in rule 7 still rejects it as a scope declaration."""
    assert path_matches('anything/at/all.py', '**')
    assert path_matches('top.py', '**')
