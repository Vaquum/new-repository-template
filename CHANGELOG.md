# v0.19.0

- Put the enforcement surfaces under code-owner review: `.github/CODEOWNERS` assigns `/governance/`, `/.github/`, `/governance.yml`, and `/requirements/` to four owners with deliberately no `*` rule, and the Protect-Main snapshot (plus all four ruleset fixtures) sets `require_code_owner_review: true`. An Actions check executes from the merge ref of the PR it judges and can be neutered by it; owner review is the one layer outside that ref. The live flag was flipped before this PR while no CODEOWNERS file existed (inert), so the ruleset drift gate stays green through delivery and enforcement activates exactly at merge — the inverse ordering of the deadlock Vaquum/Limen hit live (its S691). `require_last_push_approval: true` closes the stale-approval hole the flag alone leaves open — an owner approval granted on one revision no longer survives a later push, so sign-off-then-push cannot smuggle a change past owner review. Root `pyproject.toml` (the source the requirement sets mirror and the tool configuration the gates read) joins the owned surfaces. `governance/tests/test_codeowners.py` pins the exact owner set per surface, on-disk resolution of every owned path, the no-global-rule law, and both snapshot flags in the required lint gate.

# v0.18.0

- Hash-lock every workflow dependency install: four compiled requirement sets under `requirements/ci/` (`gate-tools` for the YAML the slice gate and bootstrap read, `dev-env` mirroring the pyproject dev extra, `build-tools` mirroring `[build-system].requires`, `runtime-env` mirroring `[project.dependencies]` — empty today, and the sole channel for the runtime dependencies the `--no-deps` editable install deliberately skips), installed everywhere with `pip install --require-hashes`; the package itself installs with `--no-build-isolation --no-deps -e .` so no job resolves a third-party package outside the pinned sets. Adopted from the law proven in Vaquum/Limen (its PR #729).
- Drop the ruleset-audit venv's bare `pip install --upgrade pip` (the audit is stdlib-only) and the `--upgrade pip` prefixes elsewhere — runner pip installs the hashed sets as-is.
- Extend `governance/tests/test_supply_chain.py` with the install law: every workflow `pip install` is either a hash-locked set or the no-resolution editable form, every compiled set is hash-complete per entry, and every `.in` source has its compiled `.txt` sibling.
- Repoint the ruff-pin contract at the new source of truth: `test_governance_config` and `test_lint_ci_contract` now resolve the ruff pin from `requirements/ci/dev-env.in`/`.txt` (still asserted equal to `governance.yml`'s `toolchain.ruff_version` and the pyproject dev extra), and the tests/lint/ruleset workflow contracts assert the hashed-install lines.

# v0.17.1

- Clear GHSA-52cp-r559-cp3m (js-yaml merge-key quadratic CPU, `>=4.0.0 <4.3.0`) from the docs-site lockfile by lifting the existing `js-yaml@^4` override to 4.3.0; the whole flagged Docusaurus chain resolved through that single pin. `npm run security:audit` and the full site check pass. No runtime behavior change.

# v0.17.0

- Pin every workflow action reference to a full commit SHA with a `# vX.Y.Z` tag comment (checkout v5.0.1, setup-python v6.3.0, setup-node v6.5.0, upload-artifact v7.0.1, setup-uv v7.6.0, codeql-action v4.37.1), so a repointed upstream tag can no longer change what runs in CI after review.
- Set `persist-credentials: false` on all fourteen checkout steps with no exception: no workflow pushes with the persisted credential (bootstrap pushes through an explicit token remote), so none may keep it. The eight base-ref `git fetch` sites authenticate per command through an `http.<host>.extraheader` `-c` flag scoped to the single fetch, so private repositories bootstrapped from this template keep working without any credential landing on disk.
- Add `governance/tests/test_supply_chain.py` to the required tests gate: zero mutable `uses:` tags, credential persistence disabled on every checkout, and an explicit `permissions:` block in every workflow — each pinned by its own assertion so regressions red the gate. Adopted from the law proven in Vaquum/Limen (its PR #696).

# v0.16.1

- Add `VAQUUM_PR_GUIDELINE.md` as the universal Vaquum PR rulebook and `VAQUUM_REPO_SPECIFICS.md` as the repo-specific appendix, pinned by checksum tests so the canonical guidance cannot silently drift. No runtime behavior change.

# v0.16.0

- Add the production documentation scaffold proven in Limen: five-section source ownership, validated product and route profiles, Docusaurus assembly, self-hosted Vaquum typography and theme, local search, route and asset verification, external-link and dependency audits, Playwright and Axe acceptance, inherited bootstrap identity, and enforcement inside the existing required lint gate.

# v0.15.0

- Add slice-gate rule 9 (PRD closure): the PR's closing set must be exactly {slice} while the parent PRD has other open slice sub-issues, exactly {slice, parent PRD} when the cited slice is the parent's last open one (resolved from the native sub-issues graph), and exactly {slice} for a parentless slice. Rule 1 now admits the second reference only under that contract, so a PRD can no longer stay silently open after its last slice merges.
- Add slice-gate rule 10 (Done Means completion): every checkbox in the cited issue's `## Done Means` section must be `- [x]` or carry `OVERRULED: <reason>` before merge; the machine-written evidence fields are not checkboxes and stay exempt pre-merge. Adopted from the downstream-proven form in Vaquum/Limen, which scopes the scan to the Done Means section rather than the whole body.
- Replace the slice template's Closeout section with Done Means: five evidence-backed checkboxes ahead of the Merge SHA / Merged PR number / required-run-id fields, and a Significance note that names the delivered workflow instead of promising an "issue-closer bot".
- Deliver `slice_closeout_guard.yml`, the promised closeout bot, fill-then-verify: a slice closed by a merged PR gets its evidence fields written from the branch rules and the head commit's check runs (failing loud when either cannot be resolved); a close with no merged PR and no evidence — or a writer failure — reopens the issue with a comment naming what is missing.
- Harden the gate's parsing for real-world issue bodies: section regexes accept `###` headings (issue-form rendering), issue bodies are CRLF-normalised before byte-equal checks, closing references are deduplicated, and gate setup failures now exit 2 instead of 1 so they cannot be mistaken for rule violations. Law 1 in `CLAUDE.md` restates the closing-set semantics.
- Close the review-round findings on the new rules: rule 10 demands exactly one Done Means section (an appended all-checked copy cannot shadow the real boxes), scans every GFM checkbox form (`-`, `*`, `+`, any indent), and rejects the literal `OVERRULED: <reason>` placeholder and unbounded `NOTOVERRULED:`-style tokens; qualified (`owner/repo#N`) and URL closing references hard-fail rule 1 because GitHub would act on them while the gate cannot fold them into the validated closing set.
- Harden the closeout guard the same way: only successful required check runs become evidence, an ambiguous duplicate Done Means section fails the writer instead of receiving evidence, a no-PR close must carry complete evidence (checked or overruled boxes, a Merge SHA reachable from `main`, a Merged PR number, and a non-empty required-run list) to stand, and any guard failure — not only the writer's — reopens the issue. Rule 9's graph lookups run only for a citation that passed rules 3-5, so a plain rule violation cannot be obscured by an API exit-2.

# v0.14.10

- Sync `.github/rulesets/main.json` with the live Protect-Main ruleset by recording the disabled `dismissal_restriction` pull-request parameter, restoring the ruleset drift gate without changing runtime behavior.

# v0.14.9

- Tighten the author-side PR workflow in `CLAUDE.md`. Open the PR first — before running the gates locally and never as a draft — so CI starts immediately and local verification never stalls without an open PR. When addressing review comments, handle every thread (blocking or not) with a named commit or a reply, then resolve it; merge already requires that server-side (`required_review_thread_resolution`), so the doc now matches the mechanism. Docs only.

# v0.14.8

- Serialize bootstrap runs with a workflow-scoped `concurrency` group (`cancel-in-progress: false`) so the repo-creation push and the `workflow_dispatch` trigger can no longer race into two parallel rename-and-merge PRs. The first run holds the lane through its rename and merge; a run queued behind it finds the repo already specialized and no-ops, exactly as the idempotency guard intends. The group deliberately differs from the `pr_checks_*` workflows, which cancel superseded runs — an interrupted bootstrap would leave a half-applied specialization, so its in-progress run is never cancelled. A new contract assertion in `test_bootstrap_workflow_contract.py` pins the group and the `false` value so the race cannot silently return.

# v0.14.7

- Finish the cohesion pass. Trim the per-gate rule lists out of the `pr_checks_cc`, `pr_checks_version`, and `pr_checks_slice` workflow headers so each gate's module docstring is the single source (the header copies had drifted — "Three"/"Six" against the real four/seven rules). Move the duplicated `find_python_files`/`_is_excluded` file-walk helpers into `_common` (`typing_gate` and `fail_loud_gate` import them now). Explain in `bootstrap_repository.py` why it deliberately keeps standalone copies of `REPO_ROOT` and `significant_lines` rather than importing `_common`. Scope law 6's line-budget wording to the `check_*` gates (the larger gate modules are held to shape by file-size balance instead). Reorder `version_gate`'s checks so execution matches the documented rule order. Make the docstring gate's forbidden-verb hint verb-agnostic, and fold the PR-template validation checkboxes into one expectation-focused item. No behavior change; full suite green.

# v0.14.6

- Tidy the test layer: the per-file `sys.path` inserts in eight gate tests are redundant now that `governance/tests/conftest.py` puts `governance/` on the path, so remove them along with the stale `SCRIPTS_DIR`/`TOOLS_DIR`/`TOOLS` constants named after the pre-v0.10.1 `scripts/`/`tools/` directories. The two contract tests that locate gate files keep the constant, renamed to the accurate `GOVERNANCE_DIR`. Every gate test now imports by bare name through the single shared path. No behavior change; full suite green.

# v0.14.5

- Consolidate `REPO_ROOT` to the single `_common` definition across every gate (no more local redefinitions or `.parent.parent` spellings), and clear residual cruft surfaced by a cohesion review: remove the bootstrap's dead pyproject-rewrite helpers (the integration-extra, `tool.uv`, `project.scripts`, and package-ignore strippers that no longer match the template's `pyproject.toml`); drop the unused `pytest-asyncio` dev dependency and the undeclared `planning` issue label; align the PR-template checklist with law 5 (every PR bumps the version and `CHANGELOG.md`, with no docs exception); scope law 6's line-budget wording to the modules that are actually budgeted; and delete a dead unreachable `raise`. No behavior change; full suite green and the bootstrap rename/de-codeql simulations stay consistent.

# v0.14.4

- Finish the `_common` consolidation the previous slice started and clear residual app specifics. `cc_gate`, `version_gate`, and `slice_gate` now import the shared `CC_RE`/`CLOSING_KEYWORD_RE` from `_common` (no more triplicated copies or dead shared constants), and the coverage-floor, coverage-ratchet, budget-ratchet, dependency-vulnerability, and diff-coverage gates route setup failures through `_common.fail_setup`. Also: spell out in law 6 the package-hygiene gates `pr_checks_lint` runs (module and docstring conventions, file-size balance, test/code ratio, no-swallowed-violations, test-fallbacks), so the constitution names every merge-blocker; define "the operator" as `zero-bang`, the approving authority; neutralize the docstring gate's data-domain wording and drop a dangling cross-repo link from the PR template; and document the no-swallowed-violations exception set as the per-repo extension point. No behavior change; full suite green and a private-bootstrap simulation stays consistent.

# v0.14.3

- Consolidate the duplicated gate helpers into a shared `governance/_common.py`: the package-root resolver (`resolve_package_dir`, previously copied across seven `check_*` gates), the significant-line counter (three copies), the setup-failure reporter (`fail_setup`), and the shared `CC_RE`/`CLOSING_KEYWORD_RE` patterns. The gates import it by bare name, exactly as they resolve siblings when run as scripts; a new `governance/tests/conftest.py` puts `governance/` on `sys.path` so the same import resolves under pytest, the bloat-gate mutation test copies `_common.py` beside a cloned gate, and pyright gets an `extraPaths` entry so the editor resolves the import (CI's type-check stays scoped to the package). No behavior change: the full suite passes, and every gate still runs green as a subprocess in a bootstrap-renamed copy.

# v0.14.2

- Tighten and align the agent-facing docs from a five-reviewer cohesion pass. Make `governance.yml` discoverable: surface it in `SETUP.md` §0, add it as the required third edit in the docs/Developer "add a gate" recipe, and give it a header comment stating it is a contract anchor (the tests pin the workflows, ruleset, pyproject, and CLAUDE.md to it), not a runtime source. Make the PR-review brief self-sufficient on approval (only `zero-bang`'s Approve unlocks merge) and drop an undefined "operator" reference. In `CLAUDE.md`, merge the duplicated fail-loud stance into one bullet, reframe the Conventions intro so it no longer restates "Beyond the laws", and fix a typo. Correct `README.md` step 1 (add `RULESET_AUDIT_TOKEN`, demote the optional label variable, point at `SETUP.md`) and disambiguate the two independent approval gates in `SETUP.md`. Docs only.

# v0.14.1

- Fix the private-repo bootstrap, broken when `governance.yml` was introduced: `disable_codeql` now also strips the `PR Checks CodeQL (python)` required check from `governance.yml`, alongside the laws, the ruleset snapshot, the workflow, and the fixtures. Without this the config contract test (`test_governance_config`, run in `pr_checks_lint`) saw the ruleset drop CodeQL while `governance.yml` kept it, and every private-without-GHAS bootstrap PR failed to merge. Add a `governance.yml` assertion to `test_codeql_fallback` so the template's own CI catches this class of regression, which it otherwise cannot (the public template always has CodeQL).

# v0.14.0

- Add `governance.yml` as the root central governance config and enforce its first settings against the live workflows, ruleset snapshot, setup docs, review authority, and tool pins through contract tests.

# v0.13.2

- Allow manual reruns of the bootstrap workflow from `main` to repair labels and the protected-main ruleset after file bootstrap has already merged, and bound the bootstrap job while it waits on PR checks.

# v0.13.1

- Consolidate the agent-facing guidelines into one canonical home each. Everything about reviewing a pull request now lives in `.github/copilot-instructions.md` (what GitHub's built-in Copilot review reads), and `CLAUDE.md` points to it for any review task instead of carrying its own copy. The generic, non-gate-enforced conventions move into `CLAUDE.md`: a new Conventions section (dependencies, logging, public surface, resources, LLM output, docs, release notes), a Fail-loud-fix-the-cause stance, and author-side PR discipline (read your own diff before requesting review; one logical change per commit). No code or gate changes.

# v0.13.0

- Add a dependency-vulnerability gate (`governance/check_dependency_vulnerabilities.py`, run in `pr_checks_lint`): the declared runtime dependencies in `[project.dependencies]` are audited with pip-audit, and any known CVE blocks merge unless covered by an active, time-boxed entry in `.github/vuln_exceptions.json` (id + reason + expiry; an expired exception no longer covers). The verdict logic is a pure, unit-tested function; the template ships with no runtime dependencies, so the gate is a vacuous pass until a derived repository declares some. Folded into the existing lint gate, so no new required check and the bijection is untouched.

# v0.12.0

- Extend the version gate (`pr_checks_version`) with two mechanizable CHANGELOG writing conventions, checked only on the new top section so older entries are never re-litigated: bullets must be imperative ("Add", not "Added") and must not leave an unfinished marker note or a stub bullet behind. Folded into the existing version gate, so no new required check and the laws<->ruleset bijection is untouched.

# v0.11.5

- Fix a regression from the idempotency guard (v0.11.4): the two bootstrap-rewrite tests assert the seed package is renamed, which only happens on the template. In a bootstrapped repo the guard correctly makes the rewrite a no-op, so those tests had nothing to rename and failed — which broke `pr_checks_lint` on every new repo's bootstrap PR, so fresh repos could no longer bootstrap. The tests now skip when no seed package is present, reading the seed names from the bootstrap module's `KNOWN_SEED_PACKAGES` (the one constant the bootstrap deliberately does not rewrite) rather than a string literal, which specialization would otherwise rewrite into the new package name and defeat the guard. Caught only by an actual end-to-end bootstrap — the template's own CI always has the seed, so it cannot surface this class of derived-repo regression.

# v0.11.4

- Make the bootstrap file rewrite idempotent. The bootstrap workflow triggers on every push to `main`, but `_apply_file_bootstrap` always re-ran `_write_module_budgets`, which regenerates budgets from the current source — so once a repository had tuned a module budget (every real slice does), each later merge re-derived different numbers, saw a diff, and opened a fresh `chore: bootstrap repository law` PR that could not auto-merge (the live ruleset now requires a review), leaving stuck PRs to accumulate. `_apply_file_bootstrap` now returns early when no seed package remains (the repository is already specialized), so re-runs are a clean no-op and open no PR. Covered by a new `test_file_bootstrap_is_idempotent` that runs the rewrite twice and asserts the second run changes nothing. Found end-to-end: every verification repo accrued one spurious bootstrap PR per merged slice.

# v0.11.3

- Move every workflow off the Node 20 GitHub Actions that GitHub is retiring (forced to Node 24 on 2026-06-16, removed 2026-09-16). Bumped to their Node-24 majors across all `.github/workflows`: `actions/checkout@v4` → `@v5`, `actions/setup-python@v4`/`@v5` → `@v6`, `actions/upload-artifact@v4` → `@v7`, `astral-sh/setup-uv@v4` → `@v7`, and `github/codeql-action/{init,autobuild,analyze}@v3` → `@v4`. Every action whose `action.yml` declared `runs.using: node20` is now on a Node-24 major; no Node-20 action remains. Surfaced by the deprecation warning on bootstrapped repos' Actions runs.

# v0.11.2

- Document in `SETUP.md` that the approving account must have **write** access to the repository: a required approval only counts from a write-access account, so a read-only approver leaves every PR stuck at "review required". Found end-to-end — a freshly bootstrapped repo could not merge any PR until the named approver (`zero-bang`) was granted push access. The platform-settings checklist and the Appendix B failure-mode table now state the requirement and the fix (per-repo collaborator or, preferably, an org team with write on all template repos).

# v0.11.1

- Repurpose `.github/copilot-instructions.md` as the single master PR-review guideline — the one brief every reviewer here (the code-review bot, an agent, or a human) works from. It is self-contained: a blocking AI-attribution stop; the "review like a senior engineer, not a linter" stance (the mechanical gates own style/types/coverage/docstrings, so review is for the semantics they cannot see); the "look beyond the diff" search (every caller, consumer, switch, and the other side of a wire format); a semantic hunt-list (correctness, environmental assumptions, identity/namespace collisions, stateful-loop idempotency, destructive ops, security surfaces, silent failures, seams, meaningful tests, empirical claims, docs-vs-implementation); the pre-post discipline (threshold test, certainty calibration, verify-the-citation, do-not-dismiss-too-fast, no invented findings); a four-tier verdict ladder (catastrophe / bad / mediocre / ok) mapped to request-changes / comment / approve; a concrete `path:line — what is wrong and why` finding format; and the posting and re-review process. `CLAUDE.md` and `AGENTS.md` now point any reviewer to it. Synthesized from established review prompts and a terse "grumpy reviewer" persona; no external links.

# v0.11.0

- Turn the fixed coverage floor into a real anti-degradation ratchet. The floor now lives in `.github/coverage_budget.json` (`line`/`branch` integer percents) instead of hard-coded constants, and the gate enforces three rules: **FLOOR** — actual coverage must clear the budgeted floor (the Limen-style absolute gate); **TRACK** — once the package is non-trivial (≥50 statements / ≥20 branches), the floor may not lag actual coverage by more than 2 points, so a real improvement must be banked and cannot silently erode back; **RATCHET** — the floor can only be *lowered* with a `[coverage-lower: <field>: <reason>]` marker in the PR body (the new `governance/check_coverage_ratchet.py`, the inverted twin of the budget ratchet), so the oracle cannot be weakened by the PR that would then slip under it. Also fixes a latent bug: the old gate read `percent_covered_branches`, a key coverage.py 7.14 does not emit, so branch coverage was never actually gated (it silently aliased to line); the gate now reads `percent_branches_covered`/`percent_statements_covered` with a fallback, and treats a zero-branch package as vacuously complete. Folded into `pr_checks_lint` — no new required check, the laws↔ruleset bijection is untouched. Starting floor ships at 50/45 so a fresh repo has on-ramp headroom; TRACK is dormant on the stub and engages as the package grows.

# v0.10.4

- Fix `disable_codeql` leaving the ruleset test fixtures stale on a private bootstrap. When the bootstrap mechanically removes CodeQL (no GitHub Advanced Security), it already strips the context from `CLAUDE.md`, the ruleset snapshot, and the workflow; it now also strips it from `governance/tests/fixtures/github/*.json`, so the ruleset-gate and privileged-audit contract tests no longer see false drift against a de-CodeQL'd snapshot. The three CodeQL-removal tests in `test_codeql_fallback` now skip when CodeQL is already absent (a re-run on an already-bootstrapped private repo), while the workflow-detection test still runs. Found by the same end-to-end smoke on a private throwaway repo.

# v0.10.3

- Fix the lint job crashing on a `slice_gate` import: PyYAML is now imported lazily, inside the one function that parses the issue template, instead of at module top — so importing `slice_gate` (which pytest does to collect `test_slice_gate`) no longer hard-requires yaml. Also pin `pyyaml>=6.0` in the `dev` extras so the toolchain venv has it explicitly rather than relying on a transitive dependency that de-scarring removed. Found by an end-to-end bootstrap smoke where the lint venv lacked yaml and `pr_checks_lint` crashed.

# v0.10.2

- Attribution scan: scrub legitimate topical references before scanning so the gate stops false-flagging the repo's own `*.md` governance files (`CLAUDE.md`, `AGENTS.md`, `copilot-instructions.md`) and the required code-review feature, while still catching real attribution (trailers, "generated with", bare vendor names elsewhere).

# v0.10.1

- Consolidate all repository-law tooling under `governance/`: the former `tools/` (the six `*_gate.py`, `bootstrap_repository.py`, `privileged_ruleset_audit.py`) and `scripts/` (the `check_*.py`) merge into `governance/`, and every gate test plus the honesty test and fixtures move to `governance/tests/`. `tests/` now holds only the app package tests. One place for all repo-template tooling. Depth is preserved (`governance/` is one level deep, `governance/tests/` two), so no `REPO_ROOT` math changed; workflows, `module_budgets.json`, the ruff per-file-ignores, the lint/honesty invocations, the bootstrap budget generator, law 6, and the slice template are all re-pointed. Full suite unchanged at 101 passing.

# v0.10.0

- Add a docstring-conventions gate (`scripts/check_docstrings.py`, run in `pr_checks_lint`) mechanizing the deterministic, domain-neutral rules from dev-docs Writing-Docstrings.md: forbidden title verbs (never Calculate/Generate/Make/Build), no `(default: ...)` in parameter descriptions, and `NOTE:` casing. Scans function/method docstrings in the package, resolves `package_root` from the single source, and fails closed. The domain-specific rules (Klines/Trades dataset phrasing, DataFrame column-name return patterns) are intentionally not enforced in an app-neutral template, and "title ends with a period" is already ruff D415.

# v0.9.0

- Add a test-fallback gate (`scripts/check_test_fallbacks.py`, run in `pr_checks_lint`): test files may not use `try`/`except` (the legitimate way to assert exception behavior is `pytest.raises`). Closes the test-hygiene gap where `fail_loud_gate` scans only the package and ruff ignores `BLE001` in tests.

# v0.8.0

- Add a diff-coverage gate (`scripts/check_diff_coverage.py`, run in `pr_checks_lint`): executable lines added to the package by a PR must be covered at >= 80% (a real per-diff floor, where the global 50/45 floor can be satisfied by old code). Resolves `package_root` from the single source and fails closed; parsing and evaluation are pure-function unit-tested.

# v0.7.0

- `cc_gate` (law 2) now also rejects AI/LLM attribution: the PR title and every non-merge commit message in range must not name an AI assistant or model (Claude, Codex, Copilot, Cursor, Gemini, ChatGPT, GPT-n, Anthropic, OpenAI, "generated with", `Co-Authored-By:` an assistant). Folded into the existing Conventional Commits gate, so no new required check or law. Mechanizes pr-prep's Phase-1b attribution scan.

# v0.6.0

- Add [`SETUP.md`](SETUP.md): the complete, agent-ready runbook for creating a new repository from the template — every secret (`REPO_BOOTSTRAP_TOKEN`, `RULESET_AUDIT_TOKEN`), variable, and token scope the rules require, why the bootstrap token must be a PAT/App (not `GITHUB_TOKEN`), why the secrets must be org-level, what the bootstrap does automatically, verification commands, and a failure-mode table. Linked from `CLAUDE.md`, `README.md`, and `copilot-instructions.md` so an agent finds it on first read; `docs/Developer` now points to it as the single source.
- Fix the bootstrap file rewrite to preserve `Vaquum/new-repository-template` references (provenance, the SETUP `--template` command, the label source) in every file rather than only in the bootstrap script, with an integration test.

# v0.5.4

- Replace the issue templates with Furnace's `slice.yml` and `prd.yml` (the `slice.yml` description neutralized from "one Furnace slice" to "one repository slice"); remove `incident_report.yml` and `incident_post_mortem.md`. The `.github/ISSUE_TEMPLATE/` directory now holds exactly those two templates. The slice gate and bootstrap extract the 11 Significance blockquotes from this template dynamically, so they self-adjust.

# v0.5.3

- De-scar the template: empty the runtime `dependencies` (was a full tdw/origo data stack — dagster, clickhouse, pandas, numpy, polars, …, none of which the stub package uses) and trim the `dev` extras to the actual toolchain (pytest, ruff, pyright, vulture, coverage). Zero dagster references remain.
- Bootstrap: `KNOWN_SEED_PACKAGES` is now just the real sentinel `new_repository_template` (not past app names), and the `tests/origo_source_native` test-path rewrite and the dead embedded honesty-test generator (superseded by the shipped bijection test) are removed.

# v0.5.2

- Rewrite `README.md` in the Vaquum/Limen structure (centered header, nav, About / Quick Start / Repository Law / Contributing / Using This Template / License) and replace the unfilled `{VALUE_PROPOSITION}`/`{QUICK_START}`/`{CONTRIBUTING}`/`{CITATIONS}`/`{LICENSE}` placeholders with real content, leaving only the three tokens the bootstrap fills.
- Expand `docs/Developer/README.md` to document the once-per-organization roll-out prerequisites (`REPO_BOOTSTRAP_TOKEN`, `LABEL_TEMPLATE_REPOSITORY`, `RULESET_AUDIT_TOKEN`, and the auto-set `RULESET_ID`), the CodeQL-on-private behavior, and the recipe for adding an app-specific required gate.

# v0.5.1

- Consolidate the constitution: `CLAUDE.md` is the single canonical document (now titled `# CLAUDE.md`, not `# AGENTS.md`, with Motivation folded in); `AGENTS.md` and `.github/copilot-instructions.md` are pointers to it. (A raw SHA-pin of the constitution was deliberately not added — the bootstrap mutates `CLAUDE.md` via token rewrite and `disable_codeql`, so a fixed hash would break every derived repo; the laws are instead guarded structurally by the `pr_checks_honesty` bijection.)

# v0.5.0

- Bootstrap detects CodeQL availability (public repo or GitHub Advanced Security) and, when CodeQL cannot run, mechanically removes it from the laws (renumbering), the ruleset snapshot, and the workflows in one step — keeping the laws <-> ruleset bijection satisfied — then opens a tracking issue to re-enable it. A private repo created from the template is no longer blocked forever by a required check that cannot run.
- Convert the constitution's intra-document `law N` cross-references to gate-name references so renumbering can never break the prose.

# v0.4.0

- Add `audit_main_ruleset`: a post-merge, privileged-token audit that re-checks the live `main` ruleset on every push — including `bypass_actors`, which the PR-time ruleset gate cannot observe. Resolves the ruleset id from the `RULESET_ID` repository variable and skips cleanly until bootstrap sets it. Run by `pr_checks_ruleset`'s contract suite.

# v0.3.0

- Promote the honesty gate to a written law (law 9) and make it enforce a laws <-> ruleset bijection: the contexts named in the laws must equal the required status checks exactly, so a gate cannot be added or dropped without its law and the CodeQL/honesty drift seen downstream cannot recur.
- Correct the CodeQL law annotation to the exact `PR Checks CodeQL (python)` context, and the lint law to describe the full gate (package + tools + tests + scripts, vulture, budgets, coverage floor).

# v0.2.2

- Bloat gates resolve their scan target from `typing_budget.json`'s `package_root` and fail closed when it is missing, instead of passing vacuously — closing the residue hole that silently disabled gates after a package rename.
- Coverage floor gate fails when the package root reports zero statements rather than passing vacuously.

# v0.2.1

- Make first-run repository bootstrap create and merge a bootstrap PR through protected main.

# v0.2.0

- Add the self-bootstrapping repository law template.

# v0.1.0

- Initial repository law baseline.
