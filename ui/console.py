from core.engine import InferenceEngine
from core.explainer import Explainer
from core.knowledge import KnowledgeBase

SEP = "=" * 52


class ConsoleApp:
    """
    Interfaz de consola del motor de teoremas.

    Responsabilidades:
    - Interactuar con el usuario (input/output).
    - Delegar el cálculo al InferenceEngine.
    - Delegar la explicación al Explainer.
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

            respuesta = input("\n¿Calcular otra cosa? (s/n): ").strip().lower()
            if respuesta != "s":
                print("Hasta luego.")
                break

    # ── Sesión individual ─────────────────────────────────────────────────────

    def _session(self) -> None:
        goal = self._ask_goal()
        if not goal:
            return

        known = self._ask_known_variables(goal)
        if known is None:
            return

        result = self._engine.prove(goal, known)
        print()
        print(self._explainer.explain(result, known))

    # ── Input ─────────────────────────────────────────────────────────────────

    def _ask_goal(self) -> str | None:
        """Pregunta qué variable calcular y valida que exista en el KB."""
        available = sorted(self._kb.known_goals())
        print(f"\nVariables calculables: {', '.join(available)}")

        goal = input("¿Que variable quieres calcular? ").strip()
        if not goal:
            return None

        if goal not in self._kb.known_goals():
            print(f"  [!] No hay ningun teorema que calcule '{goal}'.")
            print(f"      Variables disponibles: {', '.join(available)}")
            return None

        return goal

    def _ask_known_variables(self, goal: str) -> dict | None:
        """Pide los valores conocidos uno a uno hasta que el usuario termine."""
        print(f"\nIngresa los datos conocidos para calcular '{goal}'.")
        print("(Presiona Enter sin escribir nada para terminar.)\n")

        known = {}
        while True:
            var = input("  Variable (o Enter para terminar): ").strip()
            if not var:
                break
            if var == goal:
                print(f"  [!] '{goal}' es la variable a calcular, no un dato.")
                continue
            value_str = input(f"  Valor de '{var}': ").strip()
            try:
                known[var] = float(value_str)
            except ValueError:
                print(f"  [!] '{value_str}' no es un numero valido. Intenta de nuevo.")

        return known if known else None

    # ── Output ────────────────────────────────────────────────────────────────

    def _print_welcome(self) -> None:
        print(SEP)
        print("  Motor de Teoremas")
        print(SEP)
        print("  Ingresa un objetivo y los datos conocidos.")
        print("  El motor encontrara el teorema que aplica")
        print("  y explicara el procedimiento paso a paso.")
        print(SEP)
