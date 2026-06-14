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
