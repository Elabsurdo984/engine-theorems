from dataclasses import dataclass, field
from core.expression import Expression, ExpressionError
from core.knowledge import KnowledgeBase
from core.theorem import Theorem

MAX_DEPTH = 10  # límite de profundidad de búsqueda


# ── Estructuras de resultado ──────────────────────────────────────────────────

@dataclass
class ProofStep:
    """Representa un paso en la cadena de razonamiento."""
    theorem_name: str
    goal: str                       # variable que este paso probó
    expression_str: str             # fórmula utilizada
    numeric_value: float            # resultado numérico
    hypotheses_checked: list[str]   # descripciones de hipótesis verificadas
    context_used: dict              # valores de variables en el momento del cálculo


@dataclass
class ProofResult:
    """Resultado completo de un intento de prueba."""
    success: bool
    goal: str
    value: float | None
    steps: list[ProofStep] = field(default_factory=list)
    error: str | None = None


# ── Motor de inferencia ───────────────────────────────────────────────────────

class InferenceEngine:
    """
    Motor de inferencia con encadenamiento hacia atrás (backward chaining).

    Algoritmo:
    1. ¿El objetivo ya está en el contexto? → listo.
    2. Buscar en la KnowledgeBase todos los teoremas que producen el objetivo.
    3. Para cada candidato:
       a. Verificar todas sus hipótesis contra el contexto actual.
       b. Si la expresión necesita variables ausentes → intentar probarlas recursivamente.
       c. Si todo pasa → evaluar la expresión y registrar el paso.
    4. Retornar el primer resultado exitoso.
    """

    def __init__(self, kb: KnowledgeBase):
        self._kb = kb

    # ── API pública ───────────────────────────────────────────────────────────

    def prove(self, goal: str, known: dict) -> ProofResult:
        """
        Intenta calcular `goal` a partir de `known`.

        `known` no se modifica: se trabaja sobre una copia interna.
        """
        context = dict(known)   # copia local; se va enriqueciendo con derivados
        steps: list[ProofStep] = []

        value = self._prove_recursive(goal, context, steps, depth=0, proving=frozenset())

        if value is not None:
            return ProofResult(success=True, goal=goal, value=value, steps=steps)

        return ProofResult(
            success=False,
            goal=goal,
            value=None,
            steps=steps,
            error=(
                f"No se encontro forma de calcular '{goal}' "
                f"con los datos: {sorted(known.keys())}"
            ),
        )

    # ── Lógica interna ────────────────────────────────────────────────────────

    def _prove_recursive(
        self,
        goal: str,
        context: dict,
        steps: list[ProofStep],
        depth: int,
        proving: frozenset,         # variables que ya están siendo probadas en esta rama
    ) -> float | None:

        if depth > MAX_DEPTH:
            return None

        # Caso base: ya conocemos el valor
        if goal in context:
            return context[goal]

        # Detección de ciclos: si ya estamos intentando probar `goal`
        # en esta rama, no lo intentemos de nuevo
        if goal in proving:
            return None

        proving = proving | {goal}  # rama inmutable — no afecta otras ramas

        # Intentar cada teorema candidato en orden de registro
        for theorem in self._kb.theorems_for(goal):
            result = self._try_theorem(theorem, goal, context, steps, depth, proving)
            if result is not None:
                return result

        return None  # ningún teorema pudo probar `goal`

    def _try_theorem(
        self,
        theorem: Theorem,
        goal: str,
        context: dict,
        steps: list[ProofStep],
        depth: int,
        proving: frozenset,
    ) -> float | None:

        # ── Paso 1: verificar hipótesis ──────────────────────────────────────
        # True  → satisfecha
        # False → violada, el teorema no aplica → salir
        # None  → variables ausentes, diferir hasta tener el resultado
        verified = []
        deferred = []
        for hyp in theorem.hypotheses:
            result = hyp.verify(context)
            if result is False:
                return None          # hipótesis definitivamente violada
            elif result is True:
                verified.append(hyp.description)
            else:
                deferred.append(hyp)  # no se puede evaluar aún

        # ── Paso 2: obtener la fórmula para el objetivo ──────────────────────
        conclusion = theorem.conclusion_for(goal)
        expr = Expression(conclusion.expression)

        # ── Paso 3: probar variables faltantes recursivamente ────────────────
        missing = expr.required_variables - set(context.keys())
        for var in missing:
            sub_value = self._prove_recursive(var, context, steps, depth + 1, proving)
            if sub_value is None:
                return None  # no hay forma de obtener una variable requerida
            context[var] = sub_value  # enriquecer contexto con el derivado

        # ── Paso 4: evaluar la expresión ─────────────────────────────────────
        try:
            value = expr.evaluate(context)
        except ExpressionError:
            return None

        # ── Paso 5: verificar hipótesis diferidas con el valor calculado ─────
        # True  → satisfecha, registrar
        # False → el resultado viola la condición, descartar
        # None  → la variable sigue ausente, la hipótesis no aplica aquí
        context[goal] = value
        for hyp in deferred:
            result = hyp.verify(context)
            if result is False:
                context.pop(goal)
                return None
            elif result is True:
                verified.append(hyp.description)
            # None → ignorar, no es relevante para este cálculo
        steps.append(ProofStep(
            theorem_name=theorem.name,
            goal=goal,
            expression_str=conclusion.expression,
            numeric_value=value,
            hypotheses_checked=verified,
            context_used=dict(context),  # snapshot del contexto en este momento
        ))

        return value
