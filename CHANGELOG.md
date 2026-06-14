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
