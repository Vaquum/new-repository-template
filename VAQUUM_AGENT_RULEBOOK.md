# Vaquum Agent Rulebook

Status: canonical consolidated markdown rulebook for Vaquum agent-facing instructions as of 2026-06-14.
Scope: all current Vaquum GitHub repositories visible to `mikkokotila`; markdown and MDX only.
Method: 38 active repos cloned, 633 markdown files scanned, 113 in-scope instruction/procedure files curated.
Deduplication rule: each rule appears once; repo-specific rules are scoped with `domain:*` tags.

## Rubric

| Tag family | Meaning |
| --- | --- |
| `authority:*` | source precedence, entrypoints, routed reads, escalation |
| `task:*` | task classification, slice discipline, proof, completion |
| `github:*` | branches, commits, PRs, reviews, CI, rulesets, releases, bootstrap |
| `governance:*` | progov roles, planes, compile, evidence, runtime truth |
| `code:*` | implementation quality, style, errors, typing, environments |
| `docs:*` | documentation, changelog, release notes, RFCs |
| `ops:*` | incident, service, dependency, retention, runtime operations |
| `llm:*` | LLM protocol and research-procedure behavior |
| `review:*` | review posture and comment handling |
| `domain:*` | repository-specific product boundaries |

## Canonical Rules

### Authority And Routing

- `[authority:entrypoint]` Read the repository's agent entrypoint before work: `AGENTS.md`, `CLAUDE.md`, `Claude.md`, `.github/copilot-instructions.md`, or `AUDITOR.md` as applicable. Sources: repo root agent files and Copilot instruction files.
- `[authority:entrypoint]` Treat Copilot instruction files as routing pointers; the binding law usually lives in `AGENTS.md`, `CLAUDE.md`, `Claude.md`, `/docs`, or `/docs/Developer`. Sources: Copilot instruction files.
- `[authority:delegated-read]` Read delegated anchors when referenced, including `Project.md`, `PROJECT.md`, `SETUP.md`, `dev-docs`, and product documentation folders. If a referenced anchor is absent, report that fact instead of pretending it was read. Sources: `Limen/Claude.md`, `Simulator/CLAUDE.md`, `new-repository-template/SETUP.md`, `Praxis/Claude.md`.
- `[authority:contracts]` Machine contracts, router JSON blocks, compiler outputs, and generated verdicts outrank explanatory prose. Sources: `progov/governance/docs/Ontology.md`, `Origo/docs/Developer/Governance-Reading-Guide.md`, `Limen/AGENTS.md`.
- `[authority:prose]` Use prose docs for orientation only when a machine-readable authority exists; do not turn prose into a competing authority source. Sources: `Origo/docs/Developer/Governance-Reading-Guide.md`, `progov/governance/docs/Ontology.md`.
- `[authority:memory]` Never rely on memory, habit, grep alone, or repo folklore instead of routed reads. Sources: `progov/AGENTS.md`, `progov/CLAUDE.md`, `progov/AUDITOR.md`, `Origo/docs/Developer/Governance-Reading-Guide.md`.
- `[authority:unrouted]` If a behavior, task type, or request cannot be routed exactly, stop and report or escalate to Operator according to the local route policy. Sources: `Limen/AGENTS.md`, `progov/AGENTS.md`, `progov/CLAUDE.md`, `vaquum-fi-website/CLAUDE.md`.
- `[authority:missing-target]` If a bootstrap target, behavior target, contract, or delegated read target is missing, unreadable, or contradictory, stop and report or escalate. Sources: `progov/AGENTS.md`, `progov/CLAUDE.md`, `progov/AUDITOR.md`.
- `[authority:multi-behavior]` For requests spanning multiple routed behaviors, decompose the request, load the union of required targets, and execute only the routed parts inside role authority. Sources: `progov/AGENTS.md`, `progov/CLAUDE.md`, `progov/AUDITOR.md`.
- `[authority:operator]` If requirements, scope, gate meaning, or safe path are unclear, ask the Operator before proceeding. Sources: `Crucible/CLAUDE.md`, `Furnace/CLAUDE.md`, `Limen/Claude.md`.
- `[authority:checkpoint]` Where a repo requires checkpoint MCP, initialize it before work when available; if unavailable, state the gap and continue only if the task remains safely governed. Sources: `Nexus/Claude.md`, `Praxis/Claude.md`, `financial-model-simulator/Claude.md`, `Simulator/CLAUDE.md`, `Veritas/Claude.md`.

### Task Discipline

- `[task:classification]` Classify every work unit to exactly one primary `task_type` where a router exists. Sources: `Limen/AGENTS.md`, `Origo/AGENTS.md`, `resolvent/AGENTS.md`, `vaquum-fi-website/CLAUDE.md`.
- `[task:decomposition]` Decompose mixed requests before implementation. Sources: `Limen/AGENTS.md`, `progov/AGENTS.md`.
- `[task:runtime-touching]` Treat `runtime_touching` as an added proof obligation, not as a replacement for primary task type. Sources: `Limen/AGENTS.md`, `Origo/docs/Developer/Proof-And-Evidence-Workflow.md`.
- `[task:coverage]` Every touched authoritative surface must have routed contract coverage; no coverage means no work. Sources: `Limen/AGENTS.md`, `Origo/docs/Developer/Governance-Reading-Guide.md`.
- `[task:proof]` Use `proof` only for evidence and live validation; it must not hide implementation, runtime mutation, or contract mutation. Sources: `Limen/AGENTS.md`, `Origo/AGENTS.md`.
- `[task:planning]` Planning publishes approved scope into authoritative issues or execution backlog without runtime mutation. Sources: `Limen/AGENTS.md`, `Origo/AGENTS.md`.
- `[task:issue-authoring]` Issue authoring requires explicit Operator scope or source material and must not modify repo files or invent requirements. Sources: `Limen/AGENTS.md`.
- `[task:operator-surface]` Operator or user-visible surface changes require contract consistency and no hidden runtime assumptions. Sources: `Limen/AGENTS.md`.
- `[task:runtime-env]` Runtime environment work is limited to execution environment, delivery, CI, and toolchain contracts; it must not change business logic. Sources: `Limen/AGENTS.md`.
- `[task:correctness]` Correctness work fixes existing behavior without adding capability surface and requires regression protection. Sources: `Limen/AGENTS.md`.
- `[task:performance]` Performance work requires semantic equivalence, metric-delta evidence, and no behavior drift. Sources: `Limen/AGENTS.md`, `Origo/docs/Developer/Tests-And-Gates.md`.
- `[task:capability]` Capability work requires rule/contract registration, acceptance gate updates, and end-to-end validation. Sources: `Limen/AGENTS.md`, `Confab/docs/Developer/E2E-Policy.md`.
- `[task:slice]` A complete slice is the work order where slicing is required; work outside the slice is not done, work inside it is not skipped, and a wrong slice must be fixed before execution. Sources: `vaquum-fi-website/CLAUDE.md`, `Limen/AGENTS.md`.
- `[task:slice-issue]` New or replanned slice issues must define identity, task type, routing, objective, design, runtime scope, proof coverage, step register, risks, done means, and author checks before implementation. Sources: `Limen/AGENTS.md`.
- `[task:terminal-claim]` Do not claim done, ready, complete, or mergeable until required local end gates and authoritative CI gates pass for the exact candidate. Sources: `Limen/AGENTS.md`, `Loop/docs/developer/workflows/Development_Workflow.md`.
- `[task:report-back]` A repo-mutating task requires committed state, clean tree, current branch on remote, and an open PR before terminal report where the repo requires PR flow. Sources: `Limen/AGENTS.md`, `progov/CLAUDE.md`.
- `[task:final-output]` If a commit, review, or PR was made, report the hash or link. Sources: `Crucible/AGENTS.md`, `Furnace/AGENTS.md`, `Mill/CLAUDE.md`, `backtest_simulator/CLAUDE.md`.

### GitHub And Release Workflow

- `[github:branch]` Branch off `main`, push to a same-named remote branch, and keep the branch up to date with `main` before merge. Sources: `new-repository-template/CLAUDE.md`, `Crucible/CLAUDE.md`, `tdw-control-plane/AGENTS.md`.
- `[github:protected-main]` Never push directly to `main`, force-push, or delete a protected branch. Sources: template CLAUDE files and `tdw-control-plane/AGENTS.md`.
- `[github:agent-branch]` WA work branches start with `wa/`; GA work branches start with `ga/`; each role may have at most one active remote-tracked branch and one open/unmerged PR unless the Operator explicitly routes otherwise. Sources: `Limen/AGENTS.md`, `progov/governance/docs/Roles.md`.
- `[github:worktree]` Do not perform write work from detached HEAD, extra worktrees, temp worktrees, or local-only branches where branch discipline is active. Sources: `Limen/AGENTS.md`, `progov/CLAUDE.md`.
- `[github:commit]` Use Conventional Commits for PR titles, issue titles, and non-merge commits when the repo requires it. Allowed types are `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, and `revert`. Sources: template CLAUDE files, `Agent0/CLAUDE.md`.
- `[github:commit]` Do not batch unrelated changes into one commit. Sources: `Agent0/CLAUDE.md`.
- `[github:commit]` Do not mention AI, LLMs, Codex, Claude, or assistants in commit messages or PR titles where the newer template law applies. Sources: `new-repository-template/CLAUDE.md`, `nrt-e2e-smoke/CLAUDE.md`, `Limen/AGENTS.md`.
- `[github:pr]` Every gated PR closes exactly one open slice-labelled issue, keeps the PR title byte-equal to the issue title where required, stays inside issue `Surfaces`, and touches no `Out of Scope` path. Sources: template CLAUDE files, `Crucible/CLAUDE.md`, `Furnace/CLAUDE.md`.
- `[github:pr]` Open or update the PR as soon as the change is ready for CI, not after it feels finished; keep working while gates run. Sources: template CLAUDE files, `Limen/AGENTS.md`.
- `[github:pr]` Start the local compiler or test gate before push when required; terminal claims require that local gate to have completed on the exact pushed candidate. Sources: `Limen/AGENTS.md`, `progov/CLAUDE.md`.
- `[github:review]` Request `zero-bang` review where named as approving authority; re-request after all requested changes are addressed. Sources: template CLAUDE files.
- `[github:review]` All review threads must be resolved before merge; one approving review and one Copilot review are required where the ruleset says so. Sources: template CLAUDE files and `new-repository-template/SETUP.md`.
- `[github:review]` PR authors must first review their own full diff in GitHub before requesting review. Sources: `dev-docs/src/Making-Pull-Requests.md`.
- `[github:ci]` Each push re-runs gates; read failing gate output, fix the code or issue, and push again. If the gate is wrong, fix the gate in its own PR. Sources: template CLAUDE files.
- `[github:ci]` CI compile is authoritative for merge truth; dry run is blocking local evidence but not authoritative merge truth. Sources: `Limen/AGENTS.md`, `progov/governance/docs/Runtime-Ledger-and-Compile.md`.
- `[github:gates]` Written laws and enforced required checks must be in one-to-one agreement where the newer template law applies. Sources: `new-repository-template/CLAUDE.md`, `nrt-e2e-smoke/CLAUDE.md`.
- `[github:ruleset]` Live `main` branch protection must match `.github/rulesets/main.json`; out-of-band ruleset changes block the next PR until reconciled. Sources: template CLAUDE files.
- `[github:version]` Code-changing PRs and batches require a strictly forward SemVer version bump and a `CHANGELOG.md` entry unless local law explicitly exempts docs-only changes. Sources: template CLAUDE files, `Limen/AGENTS.md`, `dev-docs/src/Making-Pull-Requests.md`.
- `[github:release]` Release tags must use lowercase `v`; release notes must include `## Summary` and `## Details`, be accurate, and be published rather than left draft. Sources: `dev-docs/src/Making-Release.md`.
- `[github:bootstrap]` New repos from `new-repository-template` require org-level `REPO_BOOTSTRAP_TOKEN` and `RULESET_AUDIT_TOKEN`, enabled Actions, available Copilot review, and bootstrap verification. Sources: `new-repository-template/SETUP.md`, `nrt-e2e-smoke/SETUP.md`.
- `[github:bootstrap-token]` Do not use `GITHUB_TOKEN` for bootstrap PR creation or ruleset updates; use a PAT or GitHub App token with the documented scopes. Sources: `new-repository-template/SETUP.md`.
- `[github:codeql]` If CodeQL cannot run in a private repo, remove the CodeQL law, workflow, and ruleset requirement together and open the re-enable issue; later restore them in their own PR when CodeQL becomes available. Sources: `new-repository-template/SETUP.md`.

### Review Behavior

- `[review:pr]` When reviewing a PR, post each finding inline as a review comment without asking the Operator first. Sources: `Crucible/AGENTS.md`, `Furnace/AGENTS.md`, template CLAUDE files.
- `[review:issue]` When reviewing an issue, post comments in the issue thread without asking the Operator first. Sources: `Crucible/AGENTS.md`, `Furnace/AGENTS.md`.
- `[review:response]` When addressing comments on an issue or PR, either edit the original body or add a clear comment explaining the resolution or why it is not addressed. Sources: `Crucible/AGENTS.md`, `Furnace/AGENTS.md`.
- `[review:standard]` In review work, be meticulous; the opinion is the deliverable, and confirmation before posting is unnecessary when the repo says to review directly. Sources: `Crucible/AGENTS.md`, `Furnace/AGENTS.md`, `design-system/AGENTS.md`.

### Code And Engineering Quality

- `[code:root-cause]` Do not use workarounds, fallbacks, silent failures, or swallowed exceptions; find the root cause and fail loudly when required state is missing. Sources: `Agent0/CLAUDE.md`, template CLAUDE files.
- `[code:defensive-fog]` Do not add defensive-looking code for cases that do not exist, comments that narrate the obvious, or scaffolding that only makes the work look substantial. Sources: template CLAUDE files.
- `[code:synthetic-data]` Never invent synthetic data; if required real data is absent, stop and ask. Sources: template CLAUDE files, `Limen/Claude.md`, `Simulator/CLAUDE.md`.
- `[code:minimal-scope]` Touch only files demanded by the task; drive-by cleanup belongs in a separate slice. Sources: template CLAUDE files, `Limen/Claude.md`.
- `[code:simplicity]` Choose the simplest design that satisfies the requirement; added complexity must name the specific concern it solves. Sources: template CLAUDE files, `dev-docs/src/Writing-Code.md`.
- `[code:expectation]` Validate against the stated expectation, not merely whether a command ran. Sources: template CLAUDE files, `CC-Lab/CLAUDE.md`.
- `[code:output-visibility]` Do not hide callable output, script output, or sub-agent logs to save context; stay aware of running work. Sources: template CLAUDE files, `backtest_simulator/CLAUDE.md`, `design-system/CLAUDE.md`.
- `[code:long-running]` Do not repeatedly run long commands; profile repeated slow work and report the profile. In Mill, wrap potentially long queries with an interrupt before one minute. Sources: template CLAUDE files, `Mill/CLAUDE.md`.
- `[code:typing]` Do not weaken typing: no new `Any`, `cast(..., Any)`, `# type: ignore`, `# pyright: ignore`, or `# noqa`; Pyright error count must not rise. Sources: template CLAUDE files.
- `[code:exceptions]` Do not add bare `except`, empty handlers, `contextlib.suppress`, `errors='ignore'`, or equivalent silent-fallback patterns. Sources: template CLAUDE files, `dev-docs/src/Writing-Code.md`.
- `[code:lint]` Run the repo's required lint/type/test gates; where specified, Ruff 0.15.11 and Pyright must pass clean before closeout. Sources: `Agent0/CLAUDE.md`, template CLAUDE files, `Loop/docs/developer/workflows/Development_Workflow.md`.
- `[code:environment]` Deployment-specific variables must come from environment variables; `.env.example` is the required runtime secret/config contract; missing required vars fail loudly. Sources: `Agent0/CLAUDE.md`.
- `[code:venv]` Use the repo-specified virtual environment: `.venv` with Python 3.10 for the generic Project.md repos, or `mill` for Mill. Install from `requirements.txt` or `pyproject.toml` only when the repo says so. Sources: generic Claude files, `Mill/CLAUDE.md`.
- `[code:dependencies]` Limit external dependencies; prefer standard library or existing project dependencies unless the task requires more. Sources: generic Claude files, `dev-docs/src/Writing-Code.md`.
- `[code:imports]` Order imports as standard library, third-party, then local; never use wildcard imports. Sources: generic Claude files, `dev-docs/src/Writing-Code.md`.
- `[code:logging]` Use `logging.getLogger(__name__)` and do not use `print()` in library code. Sources: generic Claude files, `dev-docs/src/Writing-Code.md`.
- `[code:resources]` Use context managers for resources, avoid mutable default arguments, and prefer `pathlib` over `os.path`. Sources: generic Claude files, `dev-docs/src/Writing-Code.md`.
- `[code:api-surface]` Expose public API explicitly with `__all__` and prefix internal names with `_` where the house style applies. Sources: generic Claude files.
- `[code:naming]` Use uppercase constants, lowercase variables, and repo-local filename/function naming conventions where the house style applies. Sources: generic Claude files, `dev-docs/src/Writing-Code.md`.
- `[code:comments-docstrings]` Inline comments are rare and reserved for non-obvious decisions; examples belong in docs or tests. Add docstrings where the repo or dev-docs standard requires them; do not add ornamental comments or examples. Sources: generic Claude files, `dev-docs/src/Writing-Code.md`, `dev-docs/src/Writing-Docstrings.md`.
- `[code:docstrings]` When docstrings are required, document every parameter, return value, notable behavior, type, and terminology exactly; docs and docstrings must stay synchronized. Sources: `dev-docs/src/Writing-Docstrings.md`.
- `[code:llm-output]` LLMs may assist drafting, but raw LLM code must not be dropped into the repo; final simplification and accountability remain with the contributor. Sources: `dev-docs/src/Writing-Code.md`.

### Documentation

- `[docs:source]` Repository markdown is the canonical source for docs; site-only copies must not become the source of truth. Sources: Documentation-System files.
- `[docs:ownership]` Root `README.md` is the product home and first-success entry; `/docs` is public docs; `/docs/Developer` is contributor process; package READMEs orient inside modules. Sources: Documentation-System files.
- `[docs:single-source]` Author content once when possible; if explanation repeats, one page is canonical and other pages route to it. Sources: Documentation-System files.
- `[docs:writing]` Write precise, technical, concise, accessible, direct, product-truthful docs; prefer concrete current behavior over abstract or aspirational framing. Sources: Documentation-System files.
- `[docs:examples]` Use real runnable flows, commands, outputs, events, artifacts, and failure behavior; do not use imaginary examples as proof. Sources: Documentation-System files, `Origo/docs/Developer/Documentation-System.md`.
- `[docs:page-types]` Every docs page must fit one primary page type and include that type's required blocks: home, docs hub, guide, reference, developer page, or package README. Sources: Documentation-System files.
- `[docs:navigation]` Docs must route readers by task and link to the next useful page; package READMEs route back to canonical docs. Sources: Documentation-System files.
- `[docs:governance]` Developer docs must not mirror governance contracts as competing prose authority. Sources: `Origo/docs/Developer/Documentation-System.md`, `Origo/docs/Developer/Governance-Reading-Guide.md`.
- `[docs:site-build]` Docs-site changes require local/static build support and broken-link enforcement where the repo's docs contract says so. Sources: `Origo/docs/Developer/Documentation-System.md`, Progov docs-site docs.
- `[docs:changelog]` Changelog updates use SemVer, deterministic date headings, one blank line after headings, one atomic change per bullet, imperative verbs, exact note/breaking markers, category order, and no leftover placeholders. Sources: `dev-docs/src/Updating-Changelog.md`.
- `[docs:semver]` Bump major for breaking user-code changes, minor for compatible feature additions, and patch for compatible fixes. Sources: `dev-docs/src/Semantic-Versioning.md`.
- `[docs:rfc]` Every RFC section must contain content before implementation begins; only Work Phases may be empty in an initial product-only PRD draft. Sources: `dev-docs/src/Writing-RFC.md`.
- `[docs:release]` Release notes must be technically correct, concise in summary, specific in details, and tied to the pushed tag. Sources: `dev-docs/src/Making-Release.md`.

### Progov Governance

- `[governance:roles]` WA does work, GA changes governance, Auditor reads and reports only, and Operator gives tasks and resolves conflicts. Sources: `progov/governance/docs/Roles.md`.
- `[governance:wa]` WA may write work-plane files only and may not change governance-plane files, governance contracts, thresholds, baselines, parsers, wrappers, compiler behavior, or the judge. Sources: `progov/CLAUDE.md`, `progov/governance/docs/Roles.md`.
- `[governance:ga]` GA may write governance-plane files only, is not exempt from governance, must not bypass compile, and must not do product work as a substitute for WA. Sources: `progov/AGENTS.md`, `progov/governance/docs/Roles.md`.
- `[governance:auditor]` Auditor is read-only, may not edit files, commit, push, merge, or declare `pass`, and its outputs do not alter compiler verdicts. Sources: `progov/AUDITOR.md`.
- `[governance:planes]` Work may change what is judged; governance changes the judge; this separation exists so work cannot satisfy governance by weakening governance. Sources: `progov/governance/docs/Roles.md`, `progov/governance/docs/Ontology.md`.
- `[governance:pass]` `pass` is never hand-written by a person or agent; only the compiler may emit it. Sources: `progov/governance/docs/Ontology.md`, `progov/governance/compiler/README.md`.
- `[governance:truth]` Authoritative runtime state comes from an append-only typed event log; projections are computed views, not independent authority. Sources: `progov/governance/docs/Ontology.md`, `progov/governance/docs/Runtime-Ledger-and-Compile.md`.
- `[governance:evidence]` Evidence is admissible only through a governed channel or the compiler; raw probe artifacts are never counted evidence by themselves. Sources: `progov/governance/docs/Ontology.md`, `progov/governance/channels/README.md`.
- `[governance:coverage]` Every required claim must be covered by admissible passing evidence bound to exact named inputs and artifacts. Sources: `progov/governance/docs/Ontology.md`.
- `[governance:compile-basis]` Every verdict binds to the exact checked tree, prior log head, and active governance contract schema versions. Sources: `progov/governance/docs/Ontology.md`.
- `[governance:diagnostics]` Compile result equals the worst diagnostic class: any `error` yields `error`, else any `fail` yields `fail`, else `pass`. Sources: `progov/governance/docs/Ontology.md`.
- `[governance:dry-run]` Dry run uses the same compiler and schemas as CI but is non-authoritative and evaluates the local push-candidate tree. Sources: `progov/governance/docs/Runtime-Ledger-and-Compile.md`.
- `[governance:ci-compile]` CI compile is the authoritative PR candidate evaluation and may emit a candidate suffix, but protected append is a separate post-merge authority path. Sources: `progov/governance/docs/Runtime-Ledger-and-Compile.md`.
- `[governance:runtime-append]` Protected runtime append must reject stale candidate suffixes and validate linked verdict, attestation, base head, and ordering before accepting history. Sources: `progov/governance/docs/Installed-CLI.md`, `progov/governance/docs/Runtime-Ledger-and-Compile.md`.
- `[governance:routers]` Root routers must contain machine-valid route blocks mapping each supported role behavior to exact authoritative read targets. Sources: `progov/governance/docs/Ontology.md`, `progov/governance/docs/Roles.md`.
- `[governance:overlay]` Package-overlay bootstrap must fail fast if `AGENTS.md`, `CLAUDE.md`, `AUDITOR.md`, `governance/`, or managed `progov-*.yml` workflow paths are occupied by unrelated content. Sources: `progov/governance/docs/Project-Start-and-Plug-In.md`, `progov/governance/docs/Installed-CLI.md`.
- `[governance:host-topology]` Host topology and path classes refine plane authority; they must not override plane authority. Sources: `progov/governance/docs/Host-Topology-and-Path-Classes.md`.
- `[governance:work-namespace]` `work/` is the canonical namespace for governed work-process artifacts only; it is not the universal location of host work. Sources: `progov/governance/docs/Host-Topology-and-Path-Classes.md`.
- `[governance:templates]` Governance owns starter templates and canonical examples even when the live artifacts they orient belong to the work plane. Sources: `progov/governance/templates/README.md`, `progov/governance/docs/Ontology.md`.
- `[governance:template-drift]` When a template and contract drift apart, the template is wrong until compile proves otherwise. Sources: `progov/governance/templates/README.md`.
- `[governance:shared-core]` In package-overlay repos, shared-core governance changes must not be introduced by silent local drift; record a shared-core proposal artifact and link it to upstream progov evolution. Sources: `progov/governance/docs/Shared-Core-Proposals.md`.
- `[governance:conflict-resolution]` Resolve conflicts by investigation, ordered todo, and one-by-one clearing; do not bulk rewrite conflicts away. Sources: `progov/AGENTS.md`, `progov/CLAUDE.md`.

### Operations

- `[ops:prompting]` Ask Agent1 in four parts: goal, scope, constraints, and done signal; avoid vague urgency, risky implicit permission, and hidden acceptance criteria. Sources: `Agent1/docs/Partner/04-how-to-ask-agent1.md`.
- `[ops:dependency-vuln]` Python dependency gates fail on any vulnerability without active exception; Node gates fail at or above configured threshold. Exceptions require id, reason, expiry date, and remediation plan; expired exceptions fail CI. Sources: `Agent1/docs/Developer/dependency-vulnerability-policy.md`.
- `[ops:incident]` Sev1 and Sev2 incidents require owner routing, acknowledgement targets, incident commander assignment, communication cadence, post-incident review, and corrective actions feeding tests, controls, and runbooks. Sources: `Agent1/docs/Developer/incident-response-policy.md`.
- `[ops:service-level]` Release freeze is mandatory when side-effect, duplicate, or MTTR error budgets are exhausted; exit requires containment, remediation, and green validation gates. Sources: `Agent1/docs/Developer/service-level-policy.md`.
- `[ops:git-mutation-denial]` For blocked git mutations, preserve payloads, pause retries, compare against deny/allow policy, keep deny precedence, validate targeted tests, redeploy, and confirm metrics return to baseline. Sources: `Agent1/docs/Developer/runbooks/git-mutation-policy-denials.md`.
- `[ops:retention]` Retention drift and purge work starts with validation and dry run, uses strict `< cutoff` purge semantics, requires explicit production acknowledgement, and ends only after validation and chain checks pass. Sources: `Agent1/docs/Developer/runbooks/retention-and-purge-governance.md`.
- `[ops:evidence-ledger]` Evidence artifacts must maintain claim back-links, source coverage, schema consistency, and closure metadata consistency. Sources: `resolvent/_spec/wa-agent-behavior-notes.md`.

### LLM Procedures

- `[llm:protocol-generation]` MOAP protocol generation requires two independent validations for every protocol element, decision agreement threshold 0.8, documented arbitration, LLM-native patterns only, complete meta-audit trail, and governor approval at each phase transition. Source: `LLM-Resources/src/procedures/mother-of-all-procedures.md`.
- `[llm:role-separation]` Multi-role LLM procedures require `CONTEXT_RESET` before role switches; after reset the role must not use prior role perspective. Sources: LLM procedure files.
- `[llm:state]` LLM procedures must use explicit `Store as:` state, phase gates, binary validations, checkpoints, and recoverable error procedures. Sources: LLM procedure files.
- `[llm:certainty]` Knowledge Certainty Policy classifies all information as `HIGHLY_CERTAIN` or `HIGHLY_UNCERTAIN`, preserves audit trail, and keeps the multi-agent validation structure intact. Source: `LLM-Resources/src/procedures/knowledge-certainty.md`.
- `[llm:literature-review]` GSP literature reviews require PICO framing, inclusion/exclusion criteria, independent screening, kappa thresholds, audit trail, and synthesis only from extracted evidence. Source: `LLM-Resources/src/procedures/knowledge-review.md`.
- `[llm:taxonomy]` Taxonomic systematization requires atomic concepts, semantic consistency, complete hierarchical subsumption, authoritative-source traceability, coverage monitoring, and Euclidean-style output. Source: `LLM-Resources/src/procedures/knowledge-taxonomy.md`.
- `[llm:bibliometric]` Bibliometric/scientometric scanning requires objective sentiment between -0.2 and 0.2, statistical support for trading correlations at p<0.05, complete audit trail, quality metadata, and phase checkpoints. Source: `LLM-Resources/src/procedures/knowledge-bibliometric.md`.

### Domain-Specific Rules

- `[domain:agent0]` In Agent0, protect core GitHub behavior from regression; keep `.env.example`, docs, changelog, pyproject, Render, Dockerfile, Makefile, developer docs, and tests as maintained repo contracts. Source: `Agent0/CLAUDE.md`.
- `[domain:cc-lab]` In CC-Lab, work only on the specified isolated file, run all validation through `run_pipeline`, avoid custom execution workarounds, document the journey in `CHANGELOG.md`, and do not commit new permanent files. Sources: `CC-Lab/CLAUDE.md`, `CC-Lab/README.md`.
- `[domain:confab]` In Confab, every user-facing feature change must update E2E coverage in the same PR, satisfy mode-matrix and journey-spec coverage, pass policy/matrix/full E2E order, and block review if skipped. Source: `Confab/docs/Developer/E2E-Policy.md`.
- `[domain:crucible-furnace]` In Crucible and Furnace, the repository law is the AGENTS/CLAUDE template law plus repo-specific motivation: prefer commits that improve key user paths and avoid ornamental work. Sources: `Crucible/AGENTS.md`, `Furnace/AGENTS.md`, `Crucible/CLAUDE.md`, `Furnace/CLAUDE.md`.
- `[domain:backtest-simulator]` In backtest_simulator, `bts sweep` is the main path; review every task by whether it improves `bts sweep`, keep backtest close to paper and live trading, and extend Praxis/Nexus rather than building a parallel universe. Sources: `backtest_simulator/AGENTS.md`, `backtest_simulator/CLAUDE.md`.
- `[domain:design-system]` In design-system, visual work starts from `Design-System.md`, voice work starts from `Voice-Addendum.md`, planning/coding must get Codex review before conclusion where available, and every change must preserve the design system's precision and restraint. Sources: `design-system/AGENTS.md`, `design-system/CLAUDE.md`.
- `[domain:limen]` In Limen, treat `AGENTS.md` as the WA routing surface, use task-type contracts, keep WA out of governance-plane files, use `Project.md` for current scope, and do not create a new environment. Sources: `Limen/AGENTS.md`, `Limen/Claude.md`, `Limen/Project.md`.
- `[domain:loop]` In Loop, keep the stack lock: React/Vite frontend, async FastAPI backend, API-client-only domain access, Alembic-only schema changes, code-owned feature flags, trace/log preservation, frontend boundary enforcement, required local gates, done-proof, and release hygiene. Source: `Loop/docs/developer/workflows/Development_Workflow.md`.
- `[domain:mill]` In Mill, work only between raw signal and features, use import namespace `mill`, use venv `mill`, access data only through `GetData`, use the 2024-01-01 to 2026-05-15 range, add no features unless requested, and implement direct features as high-performance Polars expressions. Source: `Mill/CLAUDE.md`.
- `[domain:mill]` In Mill, do not call GUI/app configuration a manifest; the app config endpoint is `/app-config`. Source: `Mill/CLAUDE.md`.
- `[domain:origo]` In Origo, load governance contracts with `origo.governance.contract_loader.read_contracts(task_type=...)`; use prose docs only after contracts; runtime claims need supporting and terminal proof, freshness expectations, and no contradictory observability. Sources: `Origo/AGENTS.md`, `Origo/docs/Developer/Governance-Reading-Guide.md`, `Origo/docs/Developer/Proof-And-Evidence-Workflow.md`.
- `[domain:origo]` Origo validation depends on touched surface: contract tests for governance/authority/runtime semantics, performance gate for performance claims, replay/integrity gates for runtime correctness, type/style gates for type/style, and docs-site build for docs changes. Source: `Origo/docs/Developer/Tests-And-Gates.md`.
- `[domain:simulator]` In Simulator, work on the Monte Carlo simulator in small iterative changes, avoid permanent extra files, and preserve the focused case: Bitcoin only, long only, day trading only, one position open at a time, spot only, and no leverage. Source: `Simulator/Project.md`.
- `[domain:smithy]` In Smithy, report in BLUF form, keep changes minimal, and keep ownership limited to common login, landing, header, and app proxying; do not absorb Mill/Furnace internals. Source: `Smithy/AGENTS.md`.
- `[domain:website]` In `vaquum-fi-website`, classify tasks by router taxonomy, state classification and contracts before acting, complete slicing before capability work, and execute only the slice's capability/evidence/policy layers. Source: `vaquum-fi-website/CLAUDE.md`.
- `[domain:resolvent]` In resolvent, use the developer router for proof, governance, planning, issue authoring, operator surface, runtime env, correctness, performance, and capability tasks; use the operator router for research, model-input, ingestion, simulation, report, query, gap, and world-structure tasks; undefined tasks report to Operator. Sources: `resolvent/AGENTS.md`, `resolvent/CLAUDE.md`.
- `[domain:project-md-repos]` In Nexus, Praxis, financial-model-simulator, Veritas, and similar Project.md-style repos, anchor to `Project.md` when present, use `.venv`/Python 3.10, stay strictly in scope, update changelog with SemVer, test before done, and ask when requirements are unclear. Sources: generic `Claude.md` files.
- `[domain:new-repo-template]` In new-repository-template and nrt-e2e-smoke, `CLAUDE.md` is the single canonical constitution, `AGENTS.md` points to it, and `SETUP.md` governs repository bootstrap tasks. Sources: template files.
