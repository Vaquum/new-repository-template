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
