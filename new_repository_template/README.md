# Python package

`new_repository_template` is the seed package renamed by repository bootstrap.

## Canonical documentation

The root [README](../README.md) owns the product boundary and first success. The [documentation hub](../docs/README.md) owns reader routing.

## Ownership

This package owns the repository's public Python surface. It does not own repository governance or documentation assembly.

## Public entry points

The package exports a deterministic merge-path validation marker:

```python
import new_repository_template

assert new_repository_template.probe_marker() == 'merge-path-ready'
```

## Adjacent surfaces

- `governance/` owns mechanical repository law.
- `docs-site/` owns documentation assembly and rendering.
- `tests/package/` owns public package proof.

## Read next

Start with `probe_marker()` when validating package installation and import.
