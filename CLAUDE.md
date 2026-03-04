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
core/theorem.py     # Data structures (Theorem, Hypothesis, Conclusion)
core/expression.py  # SymPy wrapper (parse, evaluate, solve)
core/knowledge.py   # KnowledgeBase with inverted index: goal -> [theorems]
core/engine.py      # Backward chaining inference engine
core/explainer.py   # Step-by-step explanation formatter
domains/geometry.py # Theorem definitions (Pythagorean theorem)
ui/console.py       # Console interface
main.py             # Entry point — registers domains, starts UI
```

## Key Design Decisions

**Backward chaining** — the engine starts from the goal and works backwards. It finds theorems that produce the goal, verifies their hypotheses, recursively proves missing variables, then evaluates the formula.

**Hypothesis tri-state** — `Hypothesis.verify()` returns `True`, `False`, or `None`:
- `True` — condition satisfied
- `False` — condition violated, theorem does not apply
- `None` — required variable not yet in context (KeyError), deferred until after computation

**SymPy as backend** — SymPy handles symbolic parsing, numeric evaluation, and equation solving. The rest of the logic (which theorem to apply, hypothesis checking, step recording) is custom.

**Inverted index** — `KnowledgeBase` indexes theorems by what variables they produce. `theorems_for("c")` is O(1).

**Immutable known dict** — `engine.prove()` works on an internal copy of `known`. The caller's dict is never mutated.

**context_used in ProofStep** — each step stores a snapshot of the context at evaluation time so the explainer can show variable substitution.

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

## Conventions

- No accented characters in user-facing strings (Windows cp1252 console encoding).
- Decimal separator is comma (`,`) not period — handled in `explainer._format_number()`.
- Each `core/` module has a corresponding `tests/test_<module>.py`.
- Tests use `pytest.approx` for float comparisons.
- Domain files contain only theorem declarations — no logic.
