from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CLOSEOUT_GUARD_WORKFLOW = REPO_ROOT / '.github/workflows/slice_closeout_guard.yml'


def test_post_merge_changelog_workflow_removed() -> None:
    assert not (REPO_ROOT / '.github/workflows/pr_post_changelog.yml').exists()


def test_slice_closeout_guard_workflow_contract() -> None:
    workflow = CLOSEOUT_GUARD_WORKFLOW.read_text(encoding='utf-8')

    assert 'issues:\n    types: [closed]' in workflow
    assert "if: contains(github.event.issue.labels.*.name, 'slice')" in workflow
    assert 'issues: write' in workflow
    assert 'closedByPullRequestsReferences' in workflow
    assert r"r'^##+ Done Means\b.*?^##+ Author Checks\b'" in workflow
    # Fill: a merged closing PR gets the evidence fields written in place.
    assert "if: steps.closing_pr.outputs.pr_number != ''" in workflow
    assert 'gh issue edit "$ISSUE_NUMBER" --repo "$GITHUB_REPOSITORY" --body-file new_body.txt' in workflow
    # Verify: an evidence-less close with no merged PR, or a writer
    # failure, reopens the issue instead of letting the close stand.
    assert 'gh issue reopen' in workflow
    assert 'if: failure() && steps.writer.outcome == \'failure\'' in workflow


def test_update_changelog_script_removed() -> None:
    assert not (REPO_ROOT / 'governance/update_changelog.py').exists()


def test_typing_gate_setup_failures_exit_2() -> None:
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / 'repo'
        shutil.copytree(
            REPO_ROOT,
            tmp,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns('.git'),
        )
        (tmp / 'pyproject.toml').write_text('not = [valid\n', encoding='utf-8')

        result = subprocess.run(
            [
                'python3',
                'governance/typing_gate.py',
                '--pyright-json',
                '/tmp/missing-pyright.json',
                '--bootstrap',
            ],
            check=False,
            capture_output=True,
            text=True,
            cwd=tmp,
        )

    assert result.returncode == 2
    assert result.stdout == ''
    assert 'typing_gate: cannot parse pyproject.toml:' in result.stderr
