#!/usr/bin/env python3
"""Fuzz the slice-gate parsers that read user-authored issue bodies.

These are the only functions in the repository fed arbitrary untrusted text:
a slice issue body is written by whoever opens the issue, and `slice_gate` is
a required merge gate. A parser that raises on malformed input turns a
badly-formatted issue into a crashed gate, which reads as infrastructure
failure rather than as the authoring mistake it is.

The invariant is narrow and deliberate: these extractors must always return,
never raise. What they return on nonsense is the gate's business; that they
return at all is this fuzzer's.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'governance'))

import atheris

with atheris.instrument_imports():
    from slice_gate import (
        extract_out_of_scope_globs,
        extract_surfaces_globs,
        find_closing_references,
    )


def one_input(data: bytes) -> None:
    """Run one fuzz case through every issue-body parser."""
    body = data.decode('utf-8', errors='replace')
    extract_surfaces_globs(body)
    extract_out_of_scope_globs(body)
    find_closing_references(body)


def main() -> None:
    """Entry point for the Atheris driver."""
    atheris.Setup(sys.argv, one_input)
    atheris.Fuzz()


if __name__ == '__main__':
    main()
