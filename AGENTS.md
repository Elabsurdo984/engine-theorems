# Repository Guidelines

## Project Structure & Module Organization
`main.py` is the entry point and wires the knowledge base and console UI. Core engine logic lives in `core/` (theorem definitions, SymPy wrapper, knowledge base, inference engine, explainer). Domain-specific theorem catalogs are in `domains/` (geometry, physics, electricity). The console interface is in `ui/console.py`. Tests live in `tests/` and are organized per module (for example, `tests/test_engine.py`, `tests/test_geometry.py`). Requirements are tracked in `requirements.txt` and `requirements-dev.txt`.

## Build, Test, and Development Commands
Use the following commands from the repo root:
```bash
python main.py
```
Runs the console application.
```bash
python -m pytest -v
```
Runs the full test suite with verbose output.
```bash
python -m pytest tests/test_engine.py -v
```
Runs a specific test module.

## Coding Style & Naming Conventions
Follow standard Python formatting with 4-space indentation. Use `snake_case` for modules, functions, and variables, and `CamelCase` for classes. User-facing strings must avoid accented characters to preserve Windows console encoding. Numbers displayed to users use a comma decimal separator (handled by `core/explainer.py`). When working with SymPy, avoid reserved symbols like `I`, `E`, `S`, `N`, `Q`, and `pi`; use lowercase alternatives (for example, `i` for current).

## Testing Guidelines
Tests use `pytest` and `pytest.approx` for floating-point comparisons. Name tests as `tests/test_<module>.py` and keep assertions focused on behavior (engine results, hypothesis checks, explainer output). Run `python -m pytest -v` before opening a PR; add new tests alongside new theorems or engine behavior changes.

## Commit & Pull Request Guidelines
Commit messages in this repo use short, imperative, sentence-case summaries (for example, “Add Newton's second law to physics domain” or “Improve CI: add syntax and import checks before running tests”). Keep commits scoped to a single change.

For pull requests, include:
1. A concise description of the change and its rationale.
2. The tests you ran (with commands).
3. Any relevant console output snippets if behavior changes.

## Domain Authoring Notes
Domain files should only declare theorems (no engine logic). Add new theorems to the module `_THEOREMS` list and register the domain in `main.py` via `build_knowledge_base()`.
