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
