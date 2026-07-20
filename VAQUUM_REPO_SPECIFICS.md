# Vaquum Repo-Specific Agent Rules

Status: appendix to [VAQUUM_PR_GUIDELINE.md](VAQUUM_PR_GUIDELINE.md).
Scope: repository-specific details that should not be promoted into universal PR guidance.
Use: apply these only in the named repository or repo family, and only after reading that repository's local entrypoint.

## Org-Level Specifics

- `[repo:review-authority]` In repositories that name `zero-bang` as the approving authority, request `zero-bang` review when opening the PR and after requested changes are addressed.
- `[repo:template-bootstrap]` Repositories created from `new-repository-template` need the documented bootstrap secrets, variables, Actions settings, review availability, and ruleset setup before the gates are reliable.
- `[repo:template-codeql]` If CodeQL cannot run in a private template-derived repo, remove the CodeQL law, workflow, required check, ruleset entry, and fixtures together; re-enable them in a later PR when available.
- `[repo:work-agent-branches]` In repositories that distinguish work-agent and governance-agent roles, use the repo's declared role branch prefixes and do not keep multiple active remote-tracked role branches unless the operator routes otherwise.
- `[repo:checkpoint]` In repositories that require checkpoint MCP, initialize it before work when available; if unavailable, state the gap and continue only if local instructions permit it.

## Repository Families

- `[repo:new-repository-template]` In `new-repository-template` and its smoke repos, `CLAUDE.md` is the canonical constitution, `AGENTS.md` points to it, and `SETUP.md` governs bootstrap tasks.
- `[repo:new-repository-template]` Template PRs close the declared slice issue, obey exact surface and out-of-scope lists, satisfy Done Means, keep written laws and required checks in bijection, and keep live branch protection aligned with `.github/rulesets/main.json`.
- `[repo:progov]` In progov-style governance repositories, machine contracts, runtime ledgers, compilers, governance router outputs, and generated verdicts are authority; prose is supporting orientation.
- `[repo:progov]` Governance-plane changes must be routed through the declared governance contracts; unrouted behavior is reported instead of invented.
- `[repo:limen]` In Limen, `AGENTS.md` is the work-agent routing surface, `Project.md` is current scope, and task-type contracts control implementation and proof.
- `[repo:origo]` In Origo, load governance contracts through the contract loader for the task type, then use prose docs only after contracts have been read.
- `[repo:origo]` Origo validation depends on touched surface: contract tests, performance gates, replay or integrity gates, type/style gates, and docs-site build as routed.
- `[repo:resolvent]` In resolvent, use the developer router for proof, governance, planning, issue-authoring, operator-surface, runtime-env, correctness, performance, and capability tasks; use the operator router for research, model-input, ingestion, simulation, report, query, gap, and world-structure tasks.
- `[repo:project-md]` In Project.md-style repos, anchor scope to `Project.md`, use the declared virtual environment and Python version, stay inside scope, update changelog with SemVer, test before done, and ask when requirements are unclear.

## Product And Application Specifics

- `[repo:agent0]` In Agent0, protect core GitHub behavior from regression and keep `.env.example`, docs, changelog, project metadata, deployment files, developer docs, and tests maintained as contracts.
- `[repo:cc-lab]` In CC-Lab, work only on the specified isolated file, run validation through `run_pipeline`, avoid custom execution workarounds, document the journey in `CHANGELOG.md`, and do not commit new permanent files.
- `[repo:confab]` In Confab, every user-facing feature change updates end-to-end coverage in the same PR and satisfies mode-matrix and journey-spec policy.
- `[repo:crucible-furnace]` In Crucible and Furnace, the repository law is the AGENTS/CLAUDE template law plus the local motivation to improve key user paths and avoid ornamental work.
- `[repo:backtest-simulator]` In backtest_simulator, `bts sweep` is the main path; judge work by whether it improves that path and extend Praxis/Nexus rather than building a parallel system.
- `[repo:design-system]` In design-system, visual work starts from `Design-System.md`, voice work starts from `Voice-Addendum.md`, and every change preserves precision and restraint.
- `[repo:loop]` In Loop, keep the stack lock: React/Vite frontend, async FastAPI backend, API-client-only domain access, Alembic-only schema changes, code-owned feature flags, trace/log preservation, frontend boundary enforcement, required local gates, done-proof, and release hygiene.
- `[repo:mill]` In Mill, work only between raw signal and features, use import namespace `mill`, use venv `mill`, access data only through `GetData`, use the declared date range, and implement direct features as high-performance Polars expressions.
- `[repo:mill]` In Mill, do not call GUI or app configuration a manifest; the app config endpoint is `/app-config`.
- `[repo:simulator]` In Simulator, keep the focused case: Bitcoin only, long only, day trading only, one open position at a time, spot only, and no leverage.
- `[repo:smithy]` In Smithy, report in BLUF form, keep changes minimal, and limit ownership to common login, landing, header, and app proxying.
- `[repo:website]` In `vaquum-fi-website`, classify tasks by router taxonomy, state classification and contracts before acting, complete slicing before capability work, and execute only the slice's capability, evidence, and policy layers.

## LLM Procedure Repositories

- `[repo:llm-procedure]` MOAP protocol generation requires independent validation, documented arbitration, LLM-native patterns only, complete meta-audit trail, and governor approval at phase transitions.
- `[repo:llm-procedure]` Multi-role LLM procedures require explicit context reset before role switches.
- `[repo:llm-procedure]` LLM procedures use explicit state, phase gates, binary validations, checkpoints, and recoverable error procedures.
- `[repo:llm-procedure]` Literature reviews, taxonomies, bibliometrics, and certainty work use their procedure-specific audit trails, inclusion rules, thresholds, and validation structures.

