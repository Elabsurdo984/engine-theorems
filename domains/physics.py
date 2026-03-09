"""
Dominio: Fisica
===============
Teoremas de fisica formal.

Para agregar un nuevo teorema:
  1. Definilo como constante siguiendo el patron existente.
  2. Agregalo a la lista _THEOREMS al final del archivo.
  3. Listo -- register(kb) lo incluira automaticamente.
"""

from core.theorem import Theorem, Hypothesis, Conclusion
from core.knowledge import KnowledgeBase


# Variables compartidas de cinematica
_VARS = {
    "v0": "velocidad inicial (m/s)",
    "v":  "velocidad final (m/s)",
    "a":  "aceleracion (m/s^2)",
    "t":  "tiempo (s)",
    "d":  "desplazamiento (m)",
}


# ── Ecuacion 1: v = v0 + a*t ──────────────────────────────────────────────────
#
# Relaciona velocidad final, inicial, aceleracion y tiempo.
# No involucra desplazamiento.

CINEMATICA_VT = Theorem(
    name="Cinematica: velocidad y tiempo",
    domain="fisica",
    description="v = v0 + a*t",
    variables=_VARS,
    hypotheses=[
        Hypothesis("t > 0"),
        Hypothesis("a != 0"),
    ],
    conclusions=[
        Conclusion("v",  "v0 + a*t",       "velocidad final",    unit="m/s"),
        Conclusion("v0", "v - a*t",         "velocidad inicial",  unit="m/s"),
        Conclusion("a",  "(v - v0) / t",    "aceleracion",        unit="m/s^2"),
        Conclusion("t",  "(v - v0) / a",    "tiempo",             unit="s"),
    ],
)


# ── Ecuacion 2: d = v0*t + a*t^2/2 ───────────────────────────────────────────
#
# Relaciona desplazamiento, velocidad inicial, aceleracion y tiempo.
# No involucra velocidad final.
# Nota: no se define conclusion para t porque requiere formula cuadratica.

CINEMATICA_DT = Theorem(
    name="Cinematica: desplazamiento y tiempo",
    domain="fisica",
    description="d = v0*t + a*t^2/2",
    variables=_VARS,
    hypotheses=[
        Hypothesis("t > 0"),
    ],
    conclusions=[
        Conclusion("d",  "v0*t + a*t**2/2",          "desplazamiento",   unit="m"),
        Conclusion("v0", "(2*d - a*t**2) / (2*t)",   "velocidad inicial", unit="m/s"),
        Conclusion("a",  "2*(d - v0*t) / t**2",      "aceleracion",      unit="m/s^2"),
    ],
)


# ── Ecuacion 3: v^2 = v0^2 + 2*a*d ───────────────────────────────────────────
#
# Relaciona velocidades, aceleracion y desplazamiento.
# No involucra tiempo -- util cuando no se conoce t.

CINEMATICA_VD = Theorem(
    name="Cinematica: velocidad y desplazamiento",
    domain="fisica",
    description="v^2 = v0^2 + 2*a*d",
    variables=_VARS,
    hypotheses=[
        Hypothesis("a != 0"),
        Hypothesis("d != 0"),
    ],
    conclusions=[
        Conclusion("v",  "sqrt(v0**2 + 2*a*d)",    "velocidad final",   unit="m/s"),
        Conclusion("v0", "sqrt(v**2 - 2*a*d)",     "velocidad inicial", unit="m/s"),
        Conclusion("a",  "(v**2 - v0**2) / (2*d)", "aceleracion",       unit="m/s^2"),
        Conclusion("d",  "(v**2 - v0**2) / (2*a)", "desplazamiento",    unit="m"),
    ],
)


# ── Ecuacion 4: d = (v0 + v)*t / 2 ───────────────────────────────────────────
#
# Desplazamiento como velocidad media por tiempo.
# Util cuando se conocen ambas velocidades y el tiempo (o el desplazamiento).

CINEMATICA_DM = Theorem(
    name="Cinematica: desplazamiento y velocidad media",
    domain="fisica",
    description="d = (v0 + v)*t / 2",
    variables=_VARS,
    hypotheses=[
        Hypothesis("t > 0"),
        Hypothesis("v0 + v != 0"),
    ],
    conclusions=[
        Conclusion("d",  "(v0 + v)*t / 2",  "desplazamiento",   unit="m"),
        Conclusion("v0", "2*d/t - v",        "velocidad inicial", unit="m/s"),
        Conclusion("v",  "2*d/t - v0",       "velocidad final",  unit="m/s"),
        Conclusion("t",  "2*d / (v0 + v)",   "tiempo",           unit="s"),
    ],
)


# ── Segunda Ley de Newton: F = m * a ──────────────────────────────────────────
#
# Relaciona fuerza, masa y aceleracion.
# Comparte la variable 'a' con cinematica: si se conocen F y m,
# el motor puede derivar 'a' y usarla automaticamente en cualquier
# ecuacion cinematica.

LEY_DE_NEWTON = Theorem(
    name="Segunda Ley de Newton",
    domain="fisica",
    description="F = m * a",
    variables={
        "F": "fuerza (N)",
        "m": "masa (kg)",
        "a": "aceleracion (m/s^2)",
    },
    hypotheses=[
        Hypothesis("m > 0"),
    ],
    conclusions=[
        Conclusion("F", "m * a",  "fuerza",       unit="N"),
        Conclusion("m", "F / a",  "masa",          unit="kg"),
        Conclusion("a", "F / m",  "aceleracion",   unit="m/s^2"),
    ],
)

# ── Energia cinetica: Ec = m * v^2 / 2 ───────────────────────────────────────
#
# Relaciona energia cinetica, masa y velocidad.
# Comparte 'm' con la Ley de Newton y 'v' con cinematica,
# lo que permite encadenamiento automatico entre teoremas.

ENERGIA_CINETICA = Theorem(
    name="Energia cinetica",
    domain="fisica",
    description="Ec = m * v^2 / 2",
    variables={
        "Ec": "energia cinetica (Joules)",
        "m": "masa (kg)",
        "v": "velocidad (m/s)",
    },
    hypotheses=[
        Hypothesis("m > 0"),
        Hypothesis("Ec > 0"),
    ],
    conclusions=[
        Conclusion("Ec", "m * v**2 / 2", "energia cinetica", unit="J"),
        Conclusion("m", "2 * Ec / v**2", "masa", unit="kg"),
        Conclusion("v", "sqrt(2 * Ec / m)", "velocidad", unit="m/s"),
    ]
)


# ── Registro ──────────────────────────────────────────────────────────────────

_THEOREMS = [
    CINEMATICA_VT,
    CINEMATICA_DT,
    CINEMATICA_VD,
    CINEMATICA_DM,
    LEY_DE_NEWTON,
    ENERGIA_CINETICA,
]


def register(kb: KnowledgeBase) -> None:
    """Registra todos los teoremas de fisica en la base de conocimiento."""
    for theorem in _THEOREMS:
        kb.register(theorem)
