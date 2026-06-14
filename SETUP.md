# SETUP.md — create a new repository from this template

**If your task is to create or bootstrap a new repository from this template, this is your runbook.** Do the steps in order. Everything the rules need to actually run is listed here — nothing else is required, and nothing here is optional unless it says so.

## TL;DR

1. **Once per organization:** create two org secrets — `REPO_BOOTSTRAP_TOKEN` and `RULESET_AUDIT_TOKEN` — and confirm Actions + Copilot code review are enabled. (Optional: set the `LABEL_TEMPLATE_REPOSITORY` org variable.)
2. **Per repository:** create it from the template. The first push to `main` self-bootstraps — renames the package, opens and merges a bootstrap PR through the gates, and applies the protected-`main` ruleset.
3. **Verify** the bootstrap run, the `RULESET_ID` variable, and the live ruleset.

The reason the secrets must be **organization** secrets (not repository secrets): creating a repo from a template makes the repository *and* its first commit on `main` in one action, which triggers the bootstrap immediately — there is no window to add a repository secret first. Org secrets are present on that first run. (If you cannot use org secrets, see [Appendix A](#appendix-a--repository-level-secrets).)

---

## 0 · Prerequisites — once per organization

### Secret: `REPO_BOOTSTRAP_TOKEN` (required)

Used by `bootstrap_repository.yml` to push the bootstrap branch, create the `slice` label and the bootstrap issue, open and merge the bootstrap PR **through the gates**, copy labels, apply the ruleset, and set the `RULESET_ID` variable.

It **must be a Personal Access Token or GitHub App token — not the built-in `GITHUB_TOKEN`** — for two reasons:
- A PR opened with `GITHUB_TOKEN` does **not** trigger the gate workflows, so the bootstrap PR could never turn green.
- `GITHUB_TOKEN` cannot create or update repository **rulesets**.

Scopes (the token's owner must be an admin of the new repository):
- **Classic PAT:** `repo`, `workflow`.
- **Fine-grained PAT** (repository permissions): Contents **RW**, Pull requests **RW**, Issues **RW**, Administration **RW** (rulesets), Variables **RW** (`RULESET_ID`), Workflows **RW** (the bootstrap branch may delete `pr_checks_codeql.yml`), Metadata **R**. Grant it access to the new repository **and** to the label-source repository (it reads that repo's labels).

```bash
# org secret, available to every repo created from the template
gh secret set REPO_BOOTSTRAP_TOKEN --org <ORG> --visibility all
# (or: --visibility selected --repos <repo1>,<repo2>)
```

### Secret: `RULESET_AUDIT_TOKEN` (required for the post-merge audit)

Used by `audit_main_ruleset.yml` on every push to `main` to read the **live ruleset including `bypass_actors`**, which the PR-time ruleset gate's token cannot observe. Kept separate from the bootstrap token on purpose: it is read-only and least-privilege.

Scopes:
- **Classic PAT:** `repo`.
- **Fine-grained PAT:** Administration **R**, Metadata **R**.

```bash
gh secret set RULESET_AUDIT_TOKEN --org <ORG> --visibility all
```

### Variable: `LABEL_TEMPLATE_REPOSITORY` (optional)

The repository whose issue labels are copied into the new repo. Defaults to `Vaquum/new-repository-template` when unset.

```bash
gh variable set LABEL_TEMPLATE_REPOSITORY --org <ORG> --body <OWNER/REPO>
```

### Platform settings to confirm

- **GitHub Actions is enabled** for new repositories in the org (some orgs disable it by default).
- **Copilot code review is available**, and there is a human who can give the **one required approval**. After bootstrap, the ruleset requires 1 approving review and a Copilot review-on-push for every PR; the constitution names `zero-bang` as the approving authority. (The bootstrap PR itself merges before the ruleset is active, so it does not need these.)
- **The approving account has write (push) access to the repository.** A required approval only counts when it comes from an account with write access — a review from a read-only account is ignored, and every PR stays blocked at "review required". Grant it per repository (`gh api -X PUT /repos/<ORG>/<NAME>/collaborators/zero-bang -f permission=push`) or, preferably, add the approver to an organization team that has write access to every repository created from the template, so new repositories are immediately mergeable.

You do **not** set `RULESET_ID` — the bootstrap sets it automatically once it applies the ruleset.

---

## 1 · Create the repository

```bash
gh repo create <ORG>/<NAME> --template Vaquum/new-repository-template --private
# use --public if the repo will be public (CodeQL then runs and stays a law)
```

The Python import package defaults to the repository name in `snake_case`. To choose a different package name, run the bootstrap with `workflow_dispatch` and pass `package_name` instead of relying on the automatic first-push run.

## 2 · What the bootstrap does automatically — do **not** do these by hand

On the first push to `main`, `bootstrap_repository.yml`:

1. Detects CodeQL availability (public repo or Advanced Security).
2. Renames the seed package to the repo's name, regenerates the typing / fail-loud / module budgets against it, fills the README tokens, and seeds the baseline package + tests + `CHANGELOG`.
3. **If CodeQL cannot run** (private without Advanced Security): removes CodeQL from the laws, the ruleset snapshot, and the workflows **together** (keeping the laws ↔ ruleset bijection intact) and opens an issue to re-enable it.
4. Opens a `slice`-labelled bootstrap PR, waits for every gate, and merges it.
5. Copies labels, applies the `Protect-Main` ruleset to `main`, and sets the `RULESET_ID` variable.

## 3 · Verify

```bash
gh run list  --repo <ORG>/<NAME> --workflow bootstrap_repository.yml   # latest run: success
gh variable list --repo <ORG>/<NAME>                                   # RULESET_ID is present
gh api repos/<ORG>/<NAME>/rulesets --jq '.[].name'                     # includes "Protect-Main"
gh label list --repo <ORG>/<NAME>                                      # includes "slice"
```

Then open a throwaway PR and confirm the required checks appear and `pr_checks_honesty` (the laws ↔ ruleset bijection) passes. Close it without merging.

## 4 · If CodeQL was removed

A repo created private-without-GHAS has an open issue titled **"ci: re-enable CodeQL when the repository can run it"**. To enable it later: make the repository public or enable GitHub Advanced Security, then follow that issue — restore `pr_checks_codeql.yml`, add the law and the `PR Checks CodeQL (python)` required check back (in their own PR), and PUT the updated snapshot to the live ruleset.

---

## Appendix A · Repository-level secrets

If you cannot set organization secrets:

1. Create the repository. The automatic first bootstrap run **will fail** with `REPO_BOOTSTRAP_TOKEN is required …` — that is expected.
2. Add `REPO_BOOTSTRAP_TOKEN` and `RULESET_AUDIT_TOKEN` as **repository** secrets.
3. Re-run the bootstrap: `gh workflow run bootstrap_repository.yml --repo <ORG>/<NAME>`.

## Appendix B · Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| `REPO_BOOTSTRAP_TOKEN is required …` | secret missing or empty on the first run | set it (org or repo) and re-run the bootstrap |
| Bootstrap PR opens but its checks never start | the token is `GITHUB_TOKEN`, or a PAT that can't trigger workflows | use a PAT / GitHub App token with `workflow` scope |
| Bootstrap finishes but `RULESET_ID` is unset / no ruleset | token lacks Administration **RW** | re-issue the token with ruleset (Administration) write, re-run |
| `audit_main_ruleset` fails: missing `bypass_actors` | `RULESET_AUDIT_TOKEN` lacks admin read | grant Administration **R** to that token |
| Labels not copied | token can't read `LABEL_TEMPLATE_REPOSITORY` | grant the token read access to that repo, or set the variable to a readable one |
| Every PR is stuck at "review required" | the approver lacks **write** access (a read-only review does not count), no approver exists, or Copilot review is unavailable | give the approver write/push access (collaborator or org team), and ensure Copilot code review is enabled |
