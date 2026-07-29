# Security Policy

## Supported Versions

Only the latest released {DISPLAY_NAME} version receives security fixes.

## Reporting a Vulnerability

Report suspected vulnerabilities privately through GitHub Security Advisories:

- https://github.com/{REPOSITORY_OWNER}/{REPOSITORY_NAME}/security/advisories/new

Do not open a public issue for a vulnerability.

Include:

- affected version or commit
- reproduction steps
- expected impact
- any logs or proof artifacts that are safe to share privately

Reporters are credited in the release notes and `CHANGELOG.md` entry of the fix unless they request otherwise.

## Verifying Release Artifacts

Every release attaches the wheel, sdist, a CycloneDX `sbom.json`, and a `provenance.intoto.jsonl` attestation bundle, with SHA-256 digests in the release body. Verify a downloaded artifact with `gh attestation verify <artifact> --repo {REPOSITORY_OWNER}/{REPOSITORY_NAME}`; the verification contract is documented in [Release Policy](docs/Developer/Release-Policy.md). Report verification mismatches through the private channel above.

## Scope

Security scope covers repository code, the governance gates, packaging, release artifacts, docs-site deployment configuration, and dependency metadata maintained in this repository.
