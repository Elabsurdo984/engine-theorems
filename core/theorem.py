from dataclasses import dataclass
from typing import Callable


@dataclass
class Hypothesis:
    description: str
    check: Callable[[dict], bool]

    def verify(self, context: dict) -> bool | None:
        """
        Evalúa la condición dado el contexto actual.

        Retorna:
          True   → condición satisfecha
          False  → condición violada (el teorema no aplica)
          None   → variables requeridas ausentes en el contexto
                   (no se puede evaluar todavía; el motor decide qué hacer)
        """
        try:
            return bool(self.check(context))
        except KeyError:
            return None   # variable ausente — diferir evaluación
        except (ZeroDivisionError, TypeError, ValueError):
            return False  # error de cálculo — hipótesis violada


@dataclass
class Conclusion:
    variable: str    # qué variable produce este teorema
    expression: str  # expresión compatible con SymPy, e.g. "sqrt(a**2 + b**2)"
    description: str # explicación en lenguaje natural
    unit: str = ""   # unidad del resultado, e.g. "m/s", "V", "W"


@dataclass
class Theorem:
    name: str
    domain: str
    description: str
    variables: dict[str, str]        # nombre -> descripción humana
    hypotheses: list[Hypothesis]
    conclusions: list[Conclusion]

    def can_prove(self, goal: str) -> bool:
        """Retorna True si este teorema puede calcular la variable `goal`."""
        return any(c.variable == goal for c in self.conclusions)

    def conclusion_for(self, goal: str) -> Conclusion | None:
        """Retorna la Conclusion que produce `goal`, o None si no aplica."""
        for c in self.conclusions:
            if c.variable == goal:
                return c
        return None
