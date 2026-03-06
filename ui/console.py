import math

from core.engine import InferenceEngine
from core.explainer import Explainer, _format_number
from core.expression import Expression
from core.knowledge import KnowledgeBase
from core.theorem import Theorem

SEP_HEAVY = "=" * 52
SEP_LIGHT = "-" * 52


class ConsoleApp:
    """
    Interfaz de consola del motor de teoremas.

    Flujo de una sesion:
      1. Elegir dominio
      2. Elegir teorema
      3. Elegir que variable calcular
      4. El sistema muestra que datos se necesitan
      5. Usuario ingresa los valores
      6. Motor calcula y explica el resultado
    """

    def __init__(self, kb: KnowledgeBase):
        self._engine = InferenceEngine(kb)
        self._explainer = Explainer()
        self._kb = kb

    # ── Punto de entrada ──────────────────────────────────────────────────────

    def run(self) -> None:
        self._print_welcome()
        while True:
            try:
                self._session()
            except KeyboardInterrupt:
                print("\n\nHasta luego.")
                break
            except Exception as e:
                print(f"\n  [!] Error inesperado: {e}")
                print("  Intenta de nuevo.")
                continue

            print()
            respuesta = input("Calcular otra cosa? (s/n): ").strip().lower()
            if respuesta != "s":
                print("Hasta luego.")
                break

    # ── Sesion ────────────────────────────────────────────────────────────────

    def _session(self) -> None:
        # Paso 1: elegir dominio
        domain = self._select_domain()
        if domain is None:
            print("  Cancelado.")
            return

        # Paso 2: elegir teorema
        theorem = self._select_theorem(domain)
        if theorem is None:
            print("  Cancelado.")
            return

        # Paso 3: elegir variable a calcular
        goal = self._select_goal(theorem)
        if goal is None:
            print("  Cancelado.")
            return

        # Paso 4 y 5: mostrar qué se necesita y pedir valores
        known = self._ask_inputs(theorem, goal)
        if known is None:
            print("  Cancelado.")
            return

        # Paso 6: calcular y explicar
        result = self._engine.prove(goal, known)
        print()
        print(self._explainer.explain(result, known))

    # ── Selección de dominio ──────────────────────────────────────────────────

    def _select_domain(self) -> str | None:
        domains = sorted({t.domain for t in self._kb.all_theorems()})

        print(f"\n{SEP_LIGHT}")
        print("  Dominios disponibles:")
        for i, domain in enumerate(domains, 1):
            print(f"    [{i}] {domain.capitalize()}")

        choice = self._pick("Selecciona un dominio", len(domains))
        if choice is None:
            return None
        return domains[choice - 1]

    # ── Selección de teorema ──────────────────────────────────────────────────

    def _select_theorem(self, domain: str) -> Theorem | None:
        theorems = self._kb.theorems_by_domain(domain)

        print(f"\n  Teoremas en {domain.capitalize()}:")
        for i, t in enumerate(theorems, 1):
            print(f"    [{i}] {t.name}")
            print(f"        {t.description}")

        choice = self._pick("Selecciona un teorema", len(theorems))
        if choice is None:
            return None
        return theorems[choice - 1]

    # ── Selección de variable objetivo ────────────────────────────────────────

    def _select_goal(self, theorem: Theorem) -> str | None:
        print(f"\n{SEP_LIGHT}")
        print(f"  {theorem.name}")
        print(f"  Variables:")
        for var, desc in theorem.variables.items():
            print(f"    {var} : {desc}")

        print()
        conclusions = theorem.conclusions
        print("  Que variable quieres calcular?")
        for i, c in enumerate(conclusions, 1):
            print(f"    [{i}] {c.variable} — {c.description}")

        choice = self._pick("Selecciona", len(conclusions))
        if choice is None:
            return None
        return conclusions[choice - 1].variable

    # ── Ingreso de datos ──────────────────────────────────────────────────────

    def _ask_inputs(self, theorem: Theorem, goal: str) -> dict | None:
        conclusion = theorem.conclusion_for(goal)
        expr = Expression(conclusion.expression)
        needed = sorted(expr.required_variables)

        print(f"\n{SEP_LIGHT}")
        print(f"  Para calcular '{goal}' necesitas proporcionar:")
        for var in needed:
            desc = theorem.variables.get(var, "")
            label = f"    {var}" + (f" ({desc})" if desc else "")
            print(label)
        print("  (Enter en cualquier campo para cancelar)")

        print()
        known = {}
        for var in needed:
            desc = theorem.variables.get(var, "")
            prompt = f"  Valor de '{var}'" + (f" ({desc})" if desc else "") + ": "
            while True:
                raw = input(prompt).strip()
                if not raw:
                    return None
                try:
                    value = float(raw.replace(",", "."))
                    if not math.isfinite(value):
                        print(f"  [!] El valor debe ser un numero finito.")
                        continue
                    known[var] = value
                    break
                except ValueError:
                    print(f"  [!] '{raw}' no es un numero valido.")

        return known

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _pick(self, prompt: str, max_choice: int) -> int | None:
        """Pide al usuario un numero entre 1 y max_choice. Retorna None si cancela."""
        while True:
            raw = input(f"\n  {prompt} (1-{max_choice}, Enter para cancelar): ").strip()
            if not raw:
                return None
            try:
                n = int(raw)
                if 1 <= n <= max_choice:
                    return n
                print(f"  [!] Ingresa un numero entre 1 y {max_choice}.")
            except ValueError:
                print(f"  [!] '{raw}' no es un numero valido.")

    # ── Bienvenida ────────────────────────────────────────────────────────────

    def _print_welcome(self) -> None:
        print(SEP_HEAVY)
        print("  Motor de Teoremas")
        print(SEP_HEAVY)
        print("  Selecciona un teorema, elige que variable")
        print("  calcular, ingresa los datos conocidos y el")
        print("  motor explicara el procedimiento paso a paso.")
        print(SEP_HEAVY)
