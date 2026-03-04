# Theorem Engine

A console program that, given known data and a goal variable, automatically finds the applicable theorem, verifies its conditions, and computes the result with a step-by-step explanation.

## Features

- Formal, extensible theorem base
- Backward chaining inference engine
- Automatic hypothesis verification
- Symbolic algebra via SymPy
- Step-by-step reasoning explanation
- Multi-domain support (geometry, algebra, physics, etc.)

## Installation

```bash
pip install -r requirements.txt
```

For development (includes pytest):

```bash
pip install -r requirements-dev.txt
```

## Usage

```bash
python main.py
```

Example session:

```
====================================================
  Motor de Teoremas
====================================================

Variables calculables: a, b, c
Que variable quieres calcular? c

Ingresa los datos conocidos para calcular 'c'.

  Variable: a
  Valor de 'a': 3
  Variable: b
  Valor de 'b': 4
  Variable:

====================================================
  Objetivo: calcular 'c'
  Datos conocidos: a=3, b=4
====================================================

Paso 1 -- Teorema de Pitagoras
  Hipotesis verificadas:
    [OK] a > 0
    [OK] b > 0
  Formula:
    c = sqrt(a**2 + b**2)
  Sustitucion:
    c = 5
  Resultado:
    c = 5
  ----------------------------------------------------

  Resultado final:
    c = 5

====================================================
```

## Project Structure

```
motor-teoremas/
├── main.py              # Entry point
├── core/
│   ├── theorem.py       # Data structures: Theorem, Hypothesis, Conclusion
│   ├── expression.py    # SymPy wrapper
│   ├── knowledge.py     # Knowledge base (inverted index)
│   ├── engine.py        # Inference engine (backward chaining)
│   └── explainer.py     # Step-by-step explanation generator
├── domains/
│   └── geometry.py      # Geometry theorems (e.g. Pythagorean theorem)
├── ui/
│   └── console.py       # Console interface
└── tests/               # Per-module tests (pytest)
```

## Adding a New Theorem

1. Open or create a file inside `domains/`.
2. Define the theorem using the framework classes:

```python
from core.theorem import Theorem, Hypothesis, Conclusion

MY_THEOREM = Theorem(
    name="My theorem",
    domain="my-domain",
    description="Brief description",
    variables={"x": "description of x", "y": "description of y"},
    hypotheses=[
        Hypothesis("x > 0", lambda ctx: ctx["x"] > 0),
    ],
    conclusions=[
        Conclusion("y", "x * 2", "y is twice x"),
    ],
)
```

3. Add the theorem to `_THEOREMS` in the same file.
4. Register the domain in `main.py`:

```python
import domains.my_domain as my_domain
my_domain.register(kb)
```

## Running Tests

```bash
python -m pytest -v
```

## Tech Stack

- Python 3.13
- SymPy — symbolic algebra
- pytest — testing
