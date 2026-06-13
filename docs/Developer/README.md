# Developer Guidelines

## General Must-Read Developer Documentation

[Vaquum Developer Docs](https://github.com/Vaquum/dev-docs/blob/main/src/README.md)

## Repository law

The binding rules for this repository — the laws, the workflow, and the code
stance — live in [`CLAUDE.md`](../../CLAUDE.md). That is the single source of
truth; this document only covers what `CLAUDE.md` does not: how the template is
rolled out and extended.

## Rolling out a new repository from the template

The template self-bootstraps. On the first push to `main` of a repository
created from it, `bootstrap_repository.yml` renames the package to the
repository's name, regenerates the typing / fail-loud / module budgets against
that package, opens a `slice`-labelled bootstrap PR, merges it through the
gates, and applies the protected-`main` ruleset.

That flow needs three things configured **once per organization** (the
bootstrap fails loud, naming the missing one, if they are absent):

| Name | Kind | Purpose |
| --- | --- | --- |
| `REPO_BOOTSTRAP_TOKEN` | secret | A token that can push a branch, open and merge a PR through branch rules, create labels, and create/update repository rulesets. The bootstrap uses it to land the bootstrap PR and apply the ruleset. |
| `LABEL_TEMPLATE_REPOSITORY` | variable | The repository whose issue labels are copied into the new repository. Defaults to `Vaquum/new-repository-template`. |
| `RULESET_AUDIT_TOKEN` | secret | A privileged token used by `audit_main_ruleset` (post-merge) to read the live ruleset including `bypass_actors`, which the PR-time gate's token cannot observe. |

`RULESET_ID` is a repository **variable** the bootstrap sets automatically once
it applies the live ruleset; the ruleset and audit gates read it. You do not set
it by hand.

### CodeQL on private repositories

CodeQL needs a public repository or GitHub Advanced Security. When the bootstrap
detects that neither is available, it removes CodeQL from the laws, the ruleset
snapshot, and the workflows **together** (so the laws ↔ ruleset bijection still
holds) and opens an issue to re-enable it. Make the repository public, or enable
Advanced Security, then follow that issue to restore it.

## Adding an app-specific required gate

A new gate (for example a deployment-contract check) only blocks merges once its
job context is a required status check. Because of the laws, that cannot ride
along in a feature slice:

1. Add the workflow under `.github/workflows/`, with a job `name:` that equals
   the status-check context you want.
2. In a PR of its own (law: ruleset changes are their own PR), add a matching
   law to [`CLAUDE.md`](../../CLAUDE.md) — its trailing `*(context)*` annotation
   must equal the context exactly — and add the same context to
   `.github/rulesets/main.json`. The `pr_checks_honesty` bijection requires the
   law and the required check to be added together.
3. Apply the matching change to the live ruleset so the `pr_checks_ruleset`
   drift gate stays green.
