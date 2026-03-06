# Theorem Engine

A console program that, given known data and a goal variable, automatically finds the applicable theorem, verifies its conditions, and computes the result with a step-by-step explanation.

## Features

- Formal, extensible theorem base
- Backward chaining inference engine
- Automatic hypothesis verification
- Symbolic algebra via SymPy
- Step-by-step reasoning with units
- Guided selection: domain → theorem → variable → inputs
- Multi-domain support (geometry, physics, electricity)

## Requirements

- **Python 3.10 or later** (uses union type syntax `X | Y` from PEP 604)
- Tested on Python 3.13

## Installation

```bash
pip install -r requirements.txt
```

For development (includes pytest and coverage):

```bash
pip install -r requirements-dev.txt
```

### Dependency management

The project uses a two-file strategy for reproducible builds:

| File | Purpose |
|---|---|
| `requirements.in` | Direct deps — edit this to add/remove packages |
| `requirements.txt` | Lock file — all deps with exact versions, do not edit |
| `requirements-dev.in` | Direct dev deps — edit this |
| `requirements-dev.txt` | Dev lock file — do not edit |

To update dependencies after editing a `.in` file:

```bash
pip install pip-tools
pip-compile requirements.in
pip-compile requirements-dev.in
```

## Usage

```bash
python main.py
```

Example session (kinematics — final velocity):

```
====================================================
  Motor de Teoremas
====================================================
  Selecciona un teorema, elige que variable
  calcular, ingresa los datos conocidos y el
  motor explicara el procedimiento paso a paso.
====================================================

----------------------------------------------------
  Dominios disponibles:
    [1] Electricidad
    [2] Fisica
    [3] Geometria

  Selecciona un dominio (1-3): 2

  Teoremas en Fisica:
    [1] Cinematica: velocidad y tiempo
        v = v0 + a*t
    [2] Cinematica: desplazamiento y tiempo
        d = v0*t + a*t^2/2
    ...

  Selecciona un teorema (1-4): 1

----------------------------------------------------
  Cinematica: velocidad y tiempo
  Variables:
    v0 : velocidad inicial (m/s)
    v  : velocidad final (m/s)
    a  : aceleracion (m/s^2)
    t  : tiempo (s)

  Que variable quieres calcular?
    [1] v  — velocidad final
    [2] v0 — velocidad inicial
    [3] a  — aceleracion
    [4] t  — tiempo

  Selecciona (1-4): 1

----------------------------------------------------
  Para calcular 'v' necesitas proporcionar:
    v0 (velocidad inicial (m/s))
    a  (aceleracion (m/s^2))
    t  (tiempo (s))

  Valor de 'v0' (velocidad inicial (m/s)): 0
  Valor de 'a' (aceleracion (m/s^2)): 10
  Valor de 't' (tiempo (s)): 3

====================================================
  Objetivo: calcular 'v'
  Datos conocidos: v0=0, a=10, t=3
====================================================

Paso 1 -- Cinematica: velocidad y tiempo
  Hipotesis verificadas:
    [OK] t > 0
    [OK] a != 0
  Formula:
    v = v0 + a*t
  Sustitucion:
    v = 30
  Resultado:
    v = 30 m/s
  ----------------------------------------------------

  Resultado final:
    v = 30 m/s

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
│   ├── geometry.py      # Pythagorean theorem, Law of Cosines
│   ├── physics.py       # Kinematics (4 equations)
│   └── electricity.py   # Ohm's Law, power equations
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
        Conclusion("y", "x * 2", "y is twice x", unit="m/s"),
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
