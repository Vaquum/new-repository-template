# Developer Guidelines

## General Must-Read Developer Documentation

[Vaquum Developer Docs](https://github.com/Vaquum/dev-docs/blob/main/src/README.md)

## Repository law

The binding rules for this repository — the laws, the workflow, and the code
stance — live in [`CLAUDE.md`](../../CLAUDE.md). That is the single source of
truth; this document only covers what `CLAUDE.md` does not: how the template is
rolled out and extended.

## Rolling out a new repository from the template

The complete setup runbook — the once-per-organization secrets and variables
(`REPO_BOOTSTRAP_TOKEN`, `RULESET_AUDIT_TOKEN`, `LABEL_TEMPLATE_REPOSITORY`),
the exact token scopes, what the bootstrap does automatically, how to verify it,
the CodeQL-on-private behavior, and every failure mode — is
[`SETUP.md`](../../SETUP.md). Follow it when creating a new repository from this
template.

## Adding an app-specific required gate

A new gate (for example a deployment-contract check) only blocks merges once its
job context is a required status check. Because of the laws, that cannot ride
along in a feature slice:

1. Add the workflow under `.github/workflows/`, with a job `name:` that equals
   the status-check context you want.
2. In a PR of its own (law: ruleset changes are their own PR), add the context
   in three places that must agree: a matching law in [`CLAUDE.md`](../../CLAUDE.md)
   — its trailing `*(context)*` annotation must equal the context exactly — the
   same context in `.github/rulesets/main.json`, and the same context in
   [`governance.yml`](../../governance.yml)'s `ruleset.required_status_checks`.
   The `pr_checks_honesty` bijection ties the law to the ruleset; `test_governance_config`
   ties the ruleset to `governance.yml`. Miss any one and the PR fails.
3. Apply the matching change to the live ruleset so the `pr_checks_ruleset`
   drift gate stays green.
