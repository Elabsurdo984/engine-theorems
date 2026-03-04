"""
Dominio: Geometría
==================
Teoremas geométricos formales.

Para agregar un nuevo teorema:
  1. Definilo como constante siguiendo el patrón de PITAGORAS.
  2. Agregalo a la lista _THEOREMS al final del archivo.
  3. Listo — register(kb) lo incluirá automáticamente.
"""

import math

from core.theorem import Theorem, Hypothesis, Conclusion
from core.knowledge import KnowledgeBase


# ── Teorema de Pitágoras ──────────────────────────────────────────────────────
#
# En todo triángulo rectángulo se cumple: a² + b² = c²
# donde c es la hipotenusa y a, b son los catetos.
#
# El teorema se define en tres variantes porque el motor trabaja
# por objetivo: dependiendo de qué variable se quiere calcular,
# se usa una fórmula distinta.

PITAGORAS = Theorem(
    name="Teorema de Pitagoras",
    domain="geometria",
    description="En un triangulo rectangulo: a^2 + b^2 = c^2",
    variables={
        "a": "cateto",
        "b": "cateto",
        "c": "hipotenusa",
    },
    hypotheses=[
        Hypothesis("a > 0", lambda ctx: ctx["a"] > 0),
        Hypothesis("b > 0", lambda ctx: ctx["b"] > 0),
        Hypothesis("c > 0", lambda ctx: ctx["c"] > 0),
        # Pitagoras es un caso especial donde C = pi/2.
        # Si el angulo C es conocido y no es pi/2, este teorema no aplica
        # y debe usarse la Ley de Cosenos en su lugar.
        Hypothesis("C = pi/2 (si se conoce)", lambda ctx: ctx.get("C", math.pi / 2) == math.pi / 2),
    ],
    conclusions=[
        Conclusion(
            variable="c",
            expression="sqrt(a**2 + b**2)",
            description="Hipotenusa a partir de los dos catetos",
        ),
        Conclusion(
            variable="a",
            expression="sqrt(c**2 - b**2)",
            description="Cateto a partir de la hipotenusa y el otro cateto",
        ),
        Conclusion(
            variable="b",
            expression="sqrt(c**2 - a**2)",
            description="Cateto a partir de la hipotenusa y el otro cateto",
        ),
    ],
)


# ── Ley de Cosenos ────────────────────────────────────────────────────────────
#
# En cualquier triangulo: c² = a² + b² - 2·a·b·cos(C)
# donde A, B, C son los angulos opuestos a los lados a, b, c (en radianes).
#
# Permite calcular un lado conociendo los otros dos y el angulo entre ellos,
# o calcular un angulo conociendo los tres lados.

LEY_DE_COSENOS = Theorem(
    name="Ley de Cosenos",
    domain="geometria",
    description="c^2 = a^2 + b^2 - 2*a*b*cos(C) para cualquier triangulo",
    variables={
        "a": "lado a",
        "b": "lado b",
        "c": "lado c",
        "A": "angulo opuesto a 'a' (radianes)",
        "B": "angulo opuesto a 'b' (radianes)",
        "C": "angulo opuesto a 'c' (radianes)",
    },
    hypotheses=[
        Hypothesis("a > 0",      lambda ctx: ctx["a"] > 0),
        Hypothesis("b > 0",      lambda ctx: ctx["b"] > 0),
        Hypothesis("c > 0",      lambda ctx: ctx["c"] > 0),
        Hypothesis("0 < A < pi", lambda ctx: 0 < ctx["A"] < math.pi),
        Hypothesis("0 < B < pi", lambda ctx: 0 < ctx["B"] < math.pi),
        Hypothesis("0 < C < pi", lambda ctx: 0 < ctx["C"] < math.pi),
    ],
    conclusions=[
        # Calcular un lado dados los otros dos y el angulo entre ellos
        Conclusion("c", "sqrt(a**2 + b**2 - 2*a*b*cos(C))", "lado c dado a, b y el angulo C"),
        Conclusion("a", "sqrt(b**2 + c**2 - 2*b*c*cos(A))", "lado a dado b, c y el angulo A"),
        Conclusion("b", "sqrt(a**2 + c**2 - 2*a*c*cos(B))", "lado b dado a, c y el angulo B"),
        # Calcular un angulo dados los tres lados
        Conclusion("C", "acos((a**2 + b**2 - c**2) / (2*a*b))", "angulo C dado los tres lados"),
        Conclusion("A", "acos((b**2 + c**2 - a**2) / (2*b*c))", "angulo A dado los tres lados"),
        Conclusion("B", "acos((a**2 + c**2 - b**2) / (2*a*c))", "angulo B dado los tres lados"),
    ],
)


# ── Registro ──────────────────────────────────────────────────────────────────

_THEOREMS = [
    PITAGORAS,
    LEY_DE_COSENOS,
]


def register(kb: KnowledgeBase) -> None:
    """Registra todos los teoremas de geometría en la base de conocimiento."""
    for theorem in _THEOREMS:
        kb.register(theorem)
