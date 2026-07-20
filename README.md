<div align="center">
  <br />
  <a href="https://github.com/Vaquum"><img src="https://github.com/Vaquum/Home/raw/main/assets/Logo.png" alt="Vaquum" width="150" /></a>
  <br />
</div>
<br />
<div align="center"><strong>{DISPLAY_NAME} — {ONE_SENTENCE_DESCRIPTION}</strong></div>

<div align="center">
  <a href="#about">About</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="docs/README.md">Documentation</a> •
  <a href="#repository-law">Repository Law</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#using-this-template">Using This Template</a> •
  <a href="#license">License</a>
</div>

<hr />

<a id="about"></a>

# {DISPLAY_NAME}

*{ONE_SENTENCE_DESCRIPTION}*

Describe {DISPLAY_NAME} here: what it does, who it is for, and the one capability it delivers. Keep it to the smallest honest description a new reader can act on.

<a id="quick-start"></a>

## Quick Start

```bash
pip install {REPOSITORY_NAME}
```

Then import the package and call its public surface. Document the smallest first success here — the one command or snippet that gives a new user a real result.

<a id="repository-law"></a>

## Repository Law

This repository is governed by **[repository law](CLAUDE.md)** — a set of mechanically-enforced gates that make every change prove its own discipline before it can merge. There is no bypass.

- Every PR closes exactly one mechanically-scoped `slice` issue and stays inside the file globs that issue declares.
- Conventional Commits, a forced version + `CHANGELOG` bump, strict typing, and fail-loud (no silent fallbacks) are enforced on every PR.
- The branch-protection ruleset is checked into the repository and drift-audited, and the written laws are kept in exact agreement with the gates that actually run.

The full constitution is [`CLAUDE.md`](CLAUDE.md).

<a id="contributing"></a>

## Contributing

Branch off `main`, open one PR per `slice` issue, and let the gates run on GitHub while you keep working. Every push re-runs every gate; the merge unlocks only when all are green and the branch is up to date with `main`. See [`CLAUDE.md`](CLAUDE.md) for the laws and [`docs/Developer`](docs/Developer/README.md) for the development model.

The inherited [documentation system](docs/Developer/Documentation-System.md) supplies the five-section source model, production site scaffold, Vaquum visual language, and required proof. Replace starter prose; keep its contracts and checks.

<a id="using-this-template"></a>

## Using This Template

This repository was generated from [`Vaquum/new-repository-template`](https://github.com/Vaquum/new-repository-template). The complete, agent-ready setup runbook — every secret, variable, and permission, with verification and failure modes — is **[SETUP.md](SETUP.md)**. In short:

1. **Once per organization:** create the `REPO_BOOTSTRAP_TOKEN` and `RULESET_AUDIT_TOKEN` org secrets (a bootstrap token that can open PRs, merge through branch rules, apply labels, and apply rulesets; and a read-only token for the post-merge ruleset audit), and optionally set the `LABEL_TEMPLATE_REPOSITORY` variable. See [`SETUP.md`](SETUP.md) for the full prerequisite list, exact scopes, and failure modes.
2. Click **Use this template** and create your repository.
3. Push to `main`. The bootstrap workflow renames the package, specializes the documentation profile, regenerates the budgets, opens a bootstrap PR, merges it through the gates, and applies the protected-`main` ruleset — then you replace starter docs with source-backed product content and open your first `slice` issue.

If the repository is private without GitHub Advanced Security, the bootstrap removes CodeQL from the laws, the ruleset, and the workflows together (keeping them in agreement) and opens an issue to re-enable it once the repository can run it.

<a id="license"></a>

## License

See [`LICENSE`](LICENSE).
