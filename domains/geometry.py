"""
Dominio: Geometría
==================
Teoremas geométricos formales.

Para agregar un nuevo teorema:
  1. Definilo como constante siguiendo el patrón de PITAGORAS.
  2. Agregalo a la lista _THEOREMS al final del archivo.
  3. Listo — register(kb) lo incluirá automáticamente.
"""

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


# ── Registro ──────────────────────────────────────────────────────────────────

_THEOREMS = [
    PITAGORAS,
]


def register(kb: KnowledgeBase) -> None:
    """Registra todos los teoremas de geometría en la base de conocimiento."""
    for theorem in _THEOREMS:
        kb.register(theorem)
