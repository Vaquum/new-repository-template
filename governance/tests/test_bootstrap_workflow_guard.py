"""The bootstrap workflow skips the template repository, and only that one.

Bootstrap specializes a fresh repository created from this template. On the
template itself there is nothing to specialize, so the run reached the step
that needs `REPO_BOOTSTRAP_TOKEN` and failed on every push to main -- forty
failures deep, which is enough noise that a real bootstrap failure had nowhere
to stand out.

The guard is a job-level `if`, the only place that skips without burning a
runner or leaving a red run. That forces the template's name to be a literal
in the workflow, because a job-level condition is evaluated before any
checkout and cannot read `governance.yml`. So the literal is a mirror, and
these tests are what stop the mirror drifting -- the same treatment the other
unavoidable mirrors get.

The direction of the guard matters more than its presence. Inverted, or
rewritten to a derived repository's own name, every derived repository would
skip its own bootstrap and look configured while being untouched.
"""
from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = REPO_ROOT / '.github/workflows/bootstrap_repository.yml'
CONFIG = REPO_ROOT / 'governance.yml'
BOOTSTRAP_SCRIPT = REPO_ROOT / 'governance/bootstrap_repository.py'


def _job() -> dict[str, object]:
    payload = yaml.safe_load(WORKFLOW.read_text(encoding='utf-8'))
    jobs = payload['jobs']
    assert isinstance(jobs, dict)
    job = jobs['bootstrap']
    assert isinstance(job, dict)
    return job


def _configured_template() -> str:
    payload = yaml.safe_load(CONFIG.read_text(encoding='utf-8'))
    value = payload['bootstrap']['label_template_repository']
    assert isinstance(value, str) and value
    return value


def test_bootstrap_job_skips_the_template_repository() -> None:
    """The job carries a condition excluding this repository by name."""
    condition = _job().get('if')
    assert isinstance(condition, str), 'bootstrap job must carry an `if:` guard'
    assert 'github.repository' in condition
    assert '!=' in condition, (
        'the guard must exclude the template, not restrict to it -- inverted, '
        'every derived repository would skip its own bootstrap'
    )
    assert _configured_template() in condition


def test_guard_matches_the_configured_template_repository() -> None:
    """The literal in the workflow equals `bootstrap.label_template_repository`.

    A job-level `if` cannot read the config, so this is the only thing holding
    the two copies together.
    """
    condition = _job().get('if')
    assert isinstance(condition, str)
    expected = f"github.repository != '{_configured_template()}'"
    assert condition.strip() == expected, (condition, expected)


def test_guard_is_job_level() -> None:
    """A step-level guard would still start a runner and report a green run.

    The point is that the run does not happen at all, and reports `skipped`
    rather than a success that would claim bootstrap ran and found nothing.
    """
    job = _job()
    assert 'if' in job
    steps = job.get('steps')
    assert isinstance(steps, list)
    guarded = [
        s for s in steps
        if isinstance(s, dict) and 'github.repository' in str(s.get('if', ''))
    ]
    assert guarded == [], 'the repository guard belongs on the job, not its steps'


def test_rename_engine_leaves_workflow_files_alone() -> None:
    """Specialization must not rewrite the literal into the new repo's name.

    If it did, a derived repository's guard would name itself and it would
    skip its own bootstrap. The exemption is what makes a literal safe here,
    so it is pinned rather than assumed.
    """
    source = BOOTSTRAP_SCRIPT.read_text(encoding='utf-8')
    assert "rel_path.startswith('.github/workflows/')" in source
    assert 'continue' in source
