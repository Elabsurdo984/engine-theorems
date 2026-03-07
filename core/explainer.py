from sympy import sympify, Symbol
from core.engine import ProofResult, ProofStep


def _format_number(value: float) -> str:
    """Muestra enteros sin decimales, flotantes con 4 cifras significativas."""
    if value == int(value):
        return str(int(value))
    return f"{value:.4g}".replace(".", ",")


def _substitute(expression_str: str, context: dict) -> str:
    """
    Reemplaza los símbolos de una expresión por sus valores numéricos.
    Ejemplo: "sqrt(a**2 + b**2)" con {a:3, b:4} → "sqrt(3**2 + 4**2)"
    """
    expr = sympify(expression_str)
    sym_context = {Symbol(k): v for k, v in context.items()}
    substituted = expr.subs(sym_context)
    # Simplificar solo la forma de mostrado, no el valor final
    return str(substituted)


class Explainer:
    """
    Convierte un ProofResult en una explicación paso a paso legible.

    No contiene lógica matemática — solo formateo y presentación.
    """

    WIDTH = 52
    SEP_HEAVY = "=" * WIDTH
    SEP_LIGHT = "-" * WIDTH

    def explain(self, result: ProofResult, known: dict) -> str:
        """Retorna la explicación completa como string listo para imprimir."""
        lines = []
        lines += self._header(result, known)

        if not result.success:
            lines += self._failure(result)
        else:
            for i, step in enumerate(result.steps, start=1):
                lines += self._step(i, step, known)
            lines += self._summary(result, result.steps[-1].unit if result.steps else "")

        lines.append(self.SEP_HEAVY)
        return "\n".join(lines)

    # ── Secciones ─────────────────────────────────────────────────────────────

    def _header(self, result: ProofResult, known: dict) -> list[str]:
        lines = [self.SEP_HEAVY]
        lines.append(f"  Objetivo: calcular '{result.goal}'")
        lines.append(f"  Datos conocidos: {self._fmt_known(known)}")
        lines.append(self.SEP_HEAVY)
        return lines

    def _step(self, n: int, step: ProofStep, known: dict) -> list[str]:
        lines = [f"\nPaso {n} -- {step.theorem_name}"]

        if step.hypotheses_checked:
            lines.append("  Hipotesis verificadas:")
            for h in step.hypotheses_checked:
                lines.append(f"    [OK] {h}")

        # Fórmula original
        lines.append("  Formula:")
        lines.append(f"    {step.goal} = {step.expression_str}")

        # Sustitución numérica (sin el goal mismo)
        ctx_without_goal = {k: v for k, v in step.context_used.items()
                            if k != step.goal}
        substituted = _substitute(step.expression_str, ctx_without_goal)
        if substituted != step.expression_str:
            try:
                substituted = _format_number(float(substituted))
            except (ValueError, TypeError):
                pass
            lines.append("  Sustitucion:")
            lines.append(f"    {step.goal} = {substituted}")

        # Resultado
        unit_str = f" {step.unit}" if step.unit else ""
        lines.append("  Resultado:")
        lines.append(f"    {step.goal} = {_format_number(step.numeric_value)}{unit_str}")
        lines.append("  " + self.SEP_LIGHT)
        return lines

    def _summary(self, result: ProofResult, unit: str = "") -> list[str]:
        unit_str = f" {unit}" if unit else ""
        return [
            "",
            "  Resultado final:",
            f"    {result.goal} = {_format_number(result.value)}{unit_str}",
            "",
        ]

    def _failure(self, result: ProofResult) -> list[str]:
        return ["", f"  [ERROR] {result.error}", ""]

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _fmt_known(self, known: dict) -> str:
        return ", ".join(f"{k}={_format_number(v)}" for k, v in known.items())
