# v0.2.2

- Bloat gates resolve their scan target from `typing_budget.json`'s `package_root` and fail closed when it is missing, instead of passing vacuously — closing the residue hole that silently disabled gates after a package rename.
- Coverage floor gate fails when the package root reports zero statements rather than passing vacuously.

# v0.2.1

- Make first-run repository bootstrap create and merge a bootstrap PR through protected main.

# v0.2.0

- Add the self-bootstrapping repository law template.

# v0.1.0

- Initial repository law baseline.
