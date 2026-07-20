# Python package

`new_repository_template` is the seed package renamed by repository bootstrap.

## Canonical documentation

The root [README](../README.md) owns the product boundary and first success. The [documentation hub](../docs/README.md) owns reader routing.

## Ownership

This package owns the repository's public Python surface. It does not own repository governance or documentation assembly.

## Public entry points

The package exports a report renderer that writes to standard output:

```python
import new_repository_template

assert callable(new_repository_template.render_report)
```

## Adjacent surfaces

- `governance/` owns mechanical repository law.
- `docs-site/` owns documentation assembly and rendering.
- `tests/package/` owns public package proof.

## Read next

Start with `render_report()` when emitting report text.
