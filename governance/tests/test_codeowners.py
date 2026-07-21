"""Code-owner review law: the enforcement surfaces are owned and the
ruleset demands owner approval for changes to them.

An Actions check can be neutered by the PR it judges -- the gate
executes from the judged merge ref. Owner review is the one layer
outside that ref, so the files whose content decides merge verdicts
carry code owners, the ruleset requires their approval, and there is
deliberately no global ``*`` rule (which would make its owner a
required approver on every PR instead of only the enforcement
surfaces).
"""
from __future__ import annotations

import json
import re

from _common import REPO_ROOT

CODEOWNERS = REPO_ROOT / '.github' / 'CODEOWNERS'
RULESET_SNAPSHOT = REPO_ROOT / '.github' / 'rulesets' / 'main.json'
ENFORCEMENT_PATHS = frozenset({
    '/governance/',
    '/.github/',
    '/governance.yml',
    '/requirements/',
})
MIN_OWNERS = 2


def _rule_lines() -> list[list[str]]:
    lines = []
    for raw in CODEOWNERS.read_text(encoding='utf-8').splitlines():
        stripped = raw.strip()
        if stripped and not stripped.startswith('#'):
            lines.append(stripped.split())
    return lines


def test_codeowners_covers_enforcement_surfaces() -> None:
    rules = _rule_lines()
    assert rules, f'{CODEOWNERS} declares no ownership rules'
    covered = {rule[0] for rule in rules}
    assert covered == ENFORCEMENT_PATHS
    for rule in rules:
        owners = rule[1:]
        assert len(owners) >= MIN_OWNERS, f'{rule[0]} needs at least {MIN_OWNERS} owners'
        assert all(re.fullmatch(r'@[\w-]+', owner) for owner in owners), rule


def test_codeowners_has_no_global_rule() -> None:
    assert all(rule[0] != '*' for rule in _rule_lines()), (
        'a global * rule makes its owner a required approver on every PR'
    )


def test_ruleset_snapshot_requires_code_owner_review() -> None:
    snapshot = json.loads(RULESET_SNAPSHOT.read_text(encoding='utf-8'))
    flags = [
        rule['parameters']['require_code_owner_review']
        for rule in snapshot['rules']
        if rule['type'] == 'pull_request'
    ]
    assert flags == [True]
