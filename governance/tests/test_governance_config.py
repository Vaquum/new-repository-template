from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path
from typing import Final

import yaml

REPO_ROOT: Final[Path] = Path(__file__).resolve().parents[2]
CONFIG_PATH: Final[Path] = REPO_ROOT / 'governance.yml'
WORKFLOWS_DIR: Final[Path] = REPO_ROOT / '.github/workflows'
RULESET_PATH: Final[Path] = REPO_ROOT / '.github/rulesets/main.json'


def _mapping(value: object, name: str) -> dict[str, object]:
    assert isinstance(value, dict), f'{name} must be a mapping'
    return {str(key): item for key, item in value.items()}


def _config() -> dict[str, object]:
    return _mapping(yaml.safe_load(CONFIG_PATH.read_text(encoding='utf-8')), 'governance.yml')


def _section(name: str) -> dict[str, object]:
    return _mapping(_config().get(name), name)


def _str(section: dict[str, object], key: str) -> str:
    value = section.get(key)
    assert isinstance(value, str), f'{key} must be a string'
    return value


def _int(section: dict[str, object], key: str) -> int:
    value = section.get(key)
    assert isinstance(value, int), f'{key} must be an integer'
    return value


def _str_list(section: dict[str, object], key: str) -> list[str]:
    value = section.get(key)
    assert isinstance(value, list), f'{key} must be a list'
    assert all(isinstance(item, str) for item in value), f'{key} must contain strings'
    return [item for item in value if isinstance(item, str)]


def _required_status_contexts() -> list[str]:
    payload = json.loads(RULESET_PATH.read_text(encoding='utf-8'))
    rules = payload['rules']
    assert isinstance(rules, list)
    for rule in rules:
        rule_map = _mapping(rule, 'ruleset rule')
        if rule_map.get('type') != 'required_status_checks':
            continue
        params = _mapping(rule_map.get('parameters'), 'required_status_checks parameters')
        checks = params.get('required_status_checks')
        assert isinstance(checks, list)
        contexts: list[str] = []
        for check in checks:
            check_map = _mapping(check, 'required status check')
            context = check_map.get('context')
            assert isinstance(context, str)
            contexts.append(context)
        return contexts
    raise AssertionError('required_status_checks rule missing from ruleset snapshot')


def _setup_python_versions() -> dict[str, list[str]]:
    versions: dict[str, list[str]] = {}
    for workflow in sorted(WORKFLOWS_DIR.glob('*.yml')):
        workflow_payload = _mapping(
            yaml.safe_load(workflow.read_text(encoding='utf-8')), workflow.name
        )
        jobs = _mapping(workflow_payload.get('jobs'), f'{workflow.name}.jobs')
        workflow_versions: list[str] = []
        for job_name, job in jobs.items():
            job_map = _mapping(job, f'{workflow.name}.{job_name}')
            steps = job_map.get('steps')
            assert isinstance(steps, list), f'{workflow.name}.{job_name}.steps must be a list'
            for step in steps:
                step_map = _mapping(step, f'{workflow.name}.{job_name}.step')
                uses = step_map.get('uses')
                if not isinstance(uses, str) or not uses.startswith('actions/setup-python@'):
                    continue
                with_config = _mapping(step_map.get('with'), f'{workflow.name}.{job_name}.with')
                version = with_config.get('python-version')
                assert isinstance(version, str), f'{workflow.name} python-version must be quoted'
                workflow_versions.append(version)
        if workflow_versions:
            versions[workflow.name] = workflow_versions
    return versions


def _requirement_pins(package: str) -> list[str]:
    # Workflows install the compiled dev-env set rather than naming the
    # tools directly, so the operator-edited source of each tool pin is
    # requirements/ci/dev-env.in.
    source = REPO_ROOT / 'requirements' / 'ci' / 'dev-env.in'
    return re.findall(
        rf'^{package}==([0-9.]+)$', source.read_text(encoding='utf-8'), re.MULTILINE
    )


def test_governance_config_schema_is_minimal() -> None:
    config = _config()

    assert config['schema_version'] == 1
    assert set(config) == {
        'schema_version',
        'runtime',
        'toolchain',
        'review',
        'slice',
        'bootstrap',
        'ruleset',
    }


def test_ruleset_required_checks_match_config() -> None:
    ruleset_config = _section('ruleset')
    ruleset_snapshot = json.loads(RULESET_PATH.read_text(encoding='utf-8'))

    assert ruleset_snapshot['name'] == _str(ruleset_config, 'name')
    assert _required_status_contexts() == _str_list(ruleset_config, 'required_status_checks')


def test_workflow_runtime_and_tooling_match_config() -> None:
    runtime = _section('runtime')
    toolchain = _section('toolchain')
    python_version = _str(runtime, 'python_version')
    ruff_version = _str(toolchain, 'ruff_version')
    pyright_version = _str(toolchain, 'pyright_version')
    pyproject = tomllib.loads((REPO_ROOT / 'pyproject.toml').read_text(encoding='utf-8'))

    assert _setup_python_versions()
    for workflow_name, versions in _setup_python_versions().items():
        assert versions == [python_version] * len(versions), workflow_name
    assert _requirement_pins('ruff') == [ruff_version]
    assert _requirement_pins('pyright') == [pyright_version]
    assert pyproject['project']['requires-python'] == f'>={python_version}'
    assert f'ruff=={ruff_version}' in pyproject['project']['optional-dependencies']['dev']
    assert f'pyright=={pyright_version}' in pyproject['project']['optional-dependencies']['dev']
    assert pyproject['tool']['pyright']['pythonVersion'] == python_version


def test_bootstrap_review_and_slice_settings_match_config() -> None:
    bootstrap = _section('bootstrap')
    review = _section('review')
    slice_config = _section('slice')
    variables = _mapping(bootstrap.get('variables'), 'bootstrap.variables')
    secrets = _mapping(bootstrap.get('secrets'), 'bootstrap.secrets')
    bootstrap_workflow = (WORKFLOWS_DIR / 'bootstrap_repository.yml').read_text(encoding='utf-8')
    slice_workflow = (WORKFLOWS_DIR / 'pr_checks_slice.yml').read_text(encoding='utf-8')
    slice_issue_workflow = (WORKFLOWS_DIR / 'pr_checks_slice_on_issue.yml').read_text(
        encoding='utf-8'
    )
    label_workflow = (WORKFLOWS_DIR / 'copy-standard-labels.yml').read_text(encoding='utf-8')
    bootstrap_script = (REPO_ROOT / 'governance/bootstrap_repository.py').read_text(
        encoding='utf-8'
    )
    laws = (REPO_ROOT / 'CLAUDE.md').read_text(encoding='utf-8')
    setup = (REPO_ROOT / 'SETUP.md').read_text(encoding='utf-8')
    issue_template = (REPO_ROOT / _str(slice_config, 'issue_template')).read_text(encoding='utf-8')

    assert f'timeout-minutes: {_int(bootstrap, "timeout_minutes")}' in bootstrap_workflow
    assert f'--label {_str(slice_config, "label")}' in bootstrap_workflow
    assert f'labels:\n  - {_str(slice_config, "label")}' in issue_template
    assert _str(slice_config, 'issue_template') in slice_workflow
    assert _str(slice_config, 'issue_template') in slice_issue_workflow
    assert _str(bootstrap, 'label_template_repository') in bootstrap_script
    assert _str(variables, 'label_template_repository') in bootstrap_workflow
    assert _str(variables, 'label_template_repository') in label_workflow
    assert _str(variables, 'ruleset_id') in setup
    assert _str(secrets, 'bootstrap_token') in bootstrap_workflow
    assert _str(secrets, 'ruleset_audit_token') in setup
    assert _str(review, 'approving_authority') in laws
    assert _str(review, 'approving_authority') in setup
