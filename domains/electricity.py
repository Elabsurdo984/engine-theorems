"""
Dominio: Electricidad
=====================
Teoremas de electricidad basica.

NOTA: La variable corriente se llama 'i' (minuscula) porque SymPy
reserva 'I' (mayuscula) como la unidad imaginaria sqrt(-1).

Para agregar un nuevo teorema:
  1. Definilo como constante siguiendo el patron existente.
  2. Agregalo a la lista _THEOREMS al final del archivo.
  3. Listo -- register(kb) lo incluira automaticamente.
"""

from core.theorem import Theorem, Hypothesis, Conclusion
from core.knowledge import KnowledgeBase


# Variables compartidas
_VARS = {
    "V": "tension (V)",
    "i": "corriente (A)",
    "R": "resistencia (Ohm)",
    "P": "potencia (W)",
}


# ── Ley de Ohm: V = i * R ────────────────────────────────────────────────────

OHM = Theorem(
    name="Ley de Ohm",
    domain="electricidad",
    description="V = i * R",
    variables=_VARS,
    hypotheses=[
        Hypothesis("R > 0", lambda ctx: ctx["R"] > 0),
        Hypothesis("i != 0", lambda ctx: ctx["i"] != 0),
    ],
    conclusions=[
        Conclusion("V", "i * R",  "tension",      unit="V"),
        Conclusion("i", "V / R",  "corriente",    unit="A"),
        Conclusion("R", "V / i",  "resistencia",  unit="Ohm"),
    ],
)


# ── Potencia: P = V * i ───────────────────────────────────────────────────────

POTENCIA_VI = Theorem(
    name="Potencia (V e i)",
    domain="electricidad",
    description="P = V * i",
    variables=_VARS,
    hypotheses=[
        Hypothesis("V != 0", lambda ctx: ctx["V"] != 0),
        Hypothesis("i != 0", lambda ctx: ctx["i"] != 0),
    ],
    conclusions=[
        Conclusion("P", "V * i",  "potencia",   unit="W"),
        Conclusion("V", "P / i",  "tension",    unit="V"),
        Conclusion("i", "P / V",  "corriente",  unit="A"),
    ],
)


# ── Potencia: P = i^2 * R ────────────────────────────────────────────────────

POTENCIA_IR = Theorem(
    name="Potencia (i y R)",
    domain="electricidad",
    description="P = i^2 * R",
    variables=_VARS,
    hypotheses=[
        Hypothesis("R > 0", lambda ctx: ctx["R"] > 0),
        Hypothesis("i != 0", lambda ctx: ctx["i"] != 0),
        Hypothesis("P > 0", lambda ctx: ctx["P"] > 0),
    ],
    conclusions=[
        Conclusion("P", "i**2 * R",      "potencia",     unit="W"),
        Conclusion("i", "sqrt(P / R)",   "corriente",    unit="A"),
        Conclusion("R", "P / i**2",      "resistencia",  unit="Ohm"),
    ],
)


# ── Potencia: P = V^2 / R ────────────────────────────────────────────────────

POTENCIA_VR = Theorem(
    name="Potencia (V y R)",
    domain="electricidad",
    description="P = V^2 / R",
    variables=_VARS,
    hypotheses=[
        Hypothesis("R > 0", lambda ctx: ctx["R"] > 0),
        Hypothesis("V != 0", lambda ctx: ctx["V"] != 0),
        Hypothesis("P > 0", lambda ctx: ctx["P"] > 0),
    ],
    conclusions=[
        Conclusion("P", "V**2 / R",      "potencia",     unit="W"),
        Conclusion("V", "sqrt(P * R)",   "tension",      unit="V"),
        Conclusion("R", "V**2 / P",      "resistencia",  unit="Ohm"),
    ],
)


# ── Registro ──────────────────────────────────────────────────────────────────

_THEOREMS = [
    OHM,
    POTENCIA_VI,
    POTENCIA_IR,
    POTENCIA_VR,
]


def register(kb: KnowledgeBase) -> None:
    """Registra todos los teoremas de electricidad en la base de conocimiento."""
    for theorem in _THEOREMS:
        kb.register(theorem)
