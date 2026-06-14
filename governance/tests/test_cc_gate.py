from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_issue_title_fetch_is_non_nullable_and_gate_has_no_none_guard() -> None:
    source = (REPO_ROOT / 'governance/cc_gate.py').read_text(encoding='utf-8')
    start = source.index('def fetch_issue_title(repo: str, number: int) -> str:')
    end = source.index('def find_closing_references(body: str) -> list[int]:')
    block = source[start:end]

    assert '-> str | None' not in block
    assert 'return None' not in block
    assert 'or None if the issue cannot be' not in block
    assert 'raise SystemExit(2)' in block
    assert 'if issue_title is not None' not in source


def _load_cc_gate():
    import importlib.util
    spec = importlib.util.spec_from_file_location('cc_gate', REPO_ROOT / 'governance/cc_gate.py')
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_attribution_hit_flags_ai_attribution() -> None:
    cc = _load_cc_gate()
    assert cc.attribution_hit('Co-Authored-By: Claude <noreply@anthropic.com>') is not None
    assert cc.attribution_hit('feat: generated with Copilot assistance') is not None
    assert cc.attribution_hit('chore: 🤖 Generated with the assistant') is not None
    assert cc.attribution_hit('refactor: address anthropic feedback') is not None


def test_attribution_hit_passes_clean_messages() -> None:
    cc = _load_cc_gate()
    assert cc.attribution_hit('feat: add the maker-fill evaluator') is None
    assert cc.attribution_hit('docs: clarify the rollout runbook') is None
    assert cc.attribution_hit('fix: bound the version read') is None
    # The repo's own governance files and the Copilot review feature are
    # exempt -- they are filenames and a feature, not authorship.
    assert cc.attribution_hit('docs: retitle CLAUDE.md and point AGENTS.md at it') is None
    assert cc.attribution_hit('feat: update copilot-instructions.md and require Copilot review') is None
