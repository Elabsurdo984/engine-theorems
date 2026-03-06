# CLAUDE.md

## Project Overview

Theorem engine: given known variables and a goal, the system finds the applicable theorem, verifies hypotheses, and computes the result with a step-by-step explanation.

## Commands

```bash
python main.py          # run the app
python -m pytest -v     # run all tests
python -m pytest tests/test_engine.py -v  # run specific module tests
```

## Architecture

```
core/theorem.py        # Data structures (Theorem, Hypothesis, Conclusion)
core/expression.py     # SymPy wrapper (parse, evaluate, solve)
core/knowledge.py      # KnowledgeBase with inverted index: goal -> [theorems]
core/engine.py         # Backward chaining inference engine
core/explainer.py      # Step-by-step explanation formatter
domains/geometry.py    # Pythagorean theorem, Law of Cosines
domains/physics.py     # Kinematics: 4 equations (v=v0+at, d=v0t+at²/2, etc.)
domains/electricity.py # Ohm's Law, 3 power equations
ui/console.py          # Console interface (guided selection flow)
main.py                # Entry point — registers domains, starts UI
```

## Key Design Decisions

**Backward chaining** — the engine starts from the goal and works backwards. It finds theorems that produce the goal, verifies their hypotheses, recursively proves missing variables, then evaluates the formula.

**Hypothesis tri-state** — `Hypothesis.verify()` returns `True`, `False`, or `None`:
- `True` — condition satisfied
- `False` — condition violated, theorem does not apply
- `None` — required variable not yet in context (KeyError), deferred until after computation. If still `None` after computation, the hypothesis is ignored (not applicable to this calculation).

**SymPy as backend** — SymPy handles symbolic parsing, numeric evaluation, and equation solving. The rest of the logic (which theorem to apply, hypothesis checking, step recording) is custom.

**Inverted index** — `KnowledgeBase` indexes theorems by what variables they produce. `theorems_for("c")` is O(1).

**Immutable known dict** — `engine.prove()` works on an internal copy of `known`. The caller's dict is never mutated.

**context_used in ProofStep** — each step stores a snapshot of the context at evaluation time so the explainer can show variable substitution.

**Cycle detection** — `_prove_recursive` receives a `proving: frozenset` of variables currently being proved in the current branch. If the goal is already in `proving`, return `None` immediately to avoid infinite recursion.

**Units** — `Conclusion` has a `unit: str = ""` field. `ProofStep` carries the unit through. The explainer appends the unit to result lines (e.g. `v = 30 m/s`).

## Adding a New Theorem

1. Create or open a file in `domains/`.
2. Define a `Theorem` instance — see `domains/geometry.py` as reference.
3. Add it to `_THEOREMS` list in that file.
4. Call `your_domain.register(kb)` in `main.py` inside `build_knowledge_base()`.

## Adding a New Domain File

Follow the pattern in `domains/geometry.py`:
- Module-level theorem constants
- `_THEOREMS` list
- `register(kb: KnowledgeBase) -> None` function

## Python Version Compatibility

- **Minimum: Python 3.10** — required for union type syntax `X | Y` (PEP 604) used throughout `core/`.
- **Tested on: Python 3.13**.
- Do not use features from Python 3.11+ (e.g. `tomllib`, `ExceptionGroup`) without updating this constraint.

## Dependency Management

Two-file strategy for reproducible installs:

- `requirements.in` / `requirements-dev.in` — direct dependencies, no version pins. Edit these.
- `requirements.txt` / `requirements-dev.txt` — full lock files including transitive deps. Do not edit manually.

To regenerate lock files after changing a `.in` file:
```bash
pip install pip-tools
pip-compile requirements.in
pip-compile requirements-dev.in
```

## Conventions

- No accented characters in user-facing strings (Windows cp1252 console encoding).
- Decimal separator is comma (`,`) not period — handled in `explainer._format_number()`.
- Each `core/` module has a corresponding `tests/test_<module>.py`.
- Tests use `pytest.approx` for float comparisons.
- Domain files contain only theorem declarations — no logic.
- SymPy reserves uppercase `I` as the imaginary unit `sqrt(-1)`. Use lowercase `i` for electric current and avoid other SymPy reserved names (`E`, `S`, `N`, `Q`, `pi`).
