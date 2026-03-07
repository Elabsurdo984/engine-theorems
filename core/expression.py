from sympy import sympify, Symbol, Eq, solve, SympifyError


class ExpressionError(Exception):
    """Se lanza cuando una expresión es inválida o no se puede evaluar."""
    pass


class Expression:
    """
    Wrapper sobre SymPy para manejar expresiones simbólicas.

    Responsabilidades:
    - Parsear un string como "sqrt(a**2 + b**2)" en una expresión SymPy.
    - Evaluar numéricamente dado un contexto de variables conocidas.
    - Reportar qué variables necesita para poder evaluarse.
    - Despejar una variable (para uso futuro del motor).
    """

    def __init__(self, expr_str: str):
        try:
            self._expr = sympify(expr_str)
        except (SympifyError, SyntaxError) as e:
            raise ExpressionError(f"Expresión inválida '{expr_str}': {e}")
        self._str = expr_str

    # ── Consultas ────────────────────────────────────────────────────────────

    @property
    def required_variables(self) -> set[str]:
        """Retorna el conjunto de variables libres que necesita la expresión."""
        return {str(s) for s in self._expr.free_symbols}

    def can_evaluate(self, context: dict) -> bool:
        """True si el contexto provee todas las variables necesarias."""
        return self.required_variables.issubset(context.keys())

    # ── Evaluación ───────────────────────────────────────────────────────────

    def evaluate(self, context: dict) -> float:
        """
        Sustituye las variables del contexto y retorna el resultado numérico.

        Lanza ExpressionError si faltan variables o el resultado no es numérico.
        """
        if not self.can_evaluate(context):
            missing = self.required_variables - context.keys()
            raise ExpressionError(f"Variables faltantes para evaluar: {missing}")

        sym_context = {Symbol(k): v for k, v in context.items()}
        result = self._expr.subs(sym_context)

        try:
            return float(result)
        except (TypeError, ValueError) as e:
            raise ExpressionError(
                f"El resultado '{result}' no es un número real."
            ) from e

    # ── Resolución simbólica ─────────────────────────────────────────────────

    def solve_for(self, var: str, value: float = 0, context: dict | None = None) -> list[float]:
        """
        Despeja `var` en la ecuación: expresión = value.

        Primero sustituye las variables conocidas del contexto,
        luego despeja `var`. Retorna una lista de soluciones reales.

        Ejemplo:
            Expression("sqrt(a**2 + b**2)").solve_for("a", value=5, context={"b": 4})
            → [3.0]
        """
        expr = self._expr

        if context:
            sym_context = {Symbol(k): v for k, v in context.items()
                           if k != var}
            expr = expr.subs(sym_context)

        sym_var = Symbol(var)
        equation = Eq(expr, value)
        solutions = solve(equation, sym_var)
        return [float(s) for s in solutions if s.is_real]

    # ── Representación ───────────────────────────────────────────────────────

    def __str__(self) -> str:
        return self._str

    def __repr__(self) -> str:
        return f"Expression('{self._str}')"
