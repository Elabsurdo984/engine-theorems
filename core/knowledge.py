from core.theorem import Theorem


class KnowledgeBase:
    """
    Registro central de teoremas.

    Mantiene un índice invertido: variable → [teoremas que la producen].
    Esto permite al motor de inferencia encontrar candidatos en O(1)
    en vez de recorrer todos los teoremas cada vez.
    """

    def __init__(self):
        self._theorems: list[Theorem] = []
        self._index: dict[str, list[Theorem]] = {}  # goal → teoremas que lo prueban

    # ── Registro ─────────────────────────────────────────────────────────────

    def register(self, theorem: Theorem) -> None:
        """Agrega un teorema a la base y actualiza el índice."""
        self._theorems.append(theorem)
        for conclusion in theorem.conclusions:
            self._index.setdefault(conclusion.variable, []).append(theorem)

    # ── Consultas ────────────────────────────────────────────────────────────

    def theorems_for(self, goal: str) -> list[Theorem]:
        """Retorna todos los teoremas capaces de probar la variable `goal`."""
        return self._index.get(goal, [])

    def all_theorems(self) -> list[Theorem]:
        """Retorna todos los teoremas registrados."""
        return list(self._theorems)

    def theorems_by_domain(self, domain: str) -> list[Theorem]:
        """Retorna los teoremas de un dominio específico."""
        return [t for t in self._theorems if t.domain == domain]

    def known_goals(self) -> set[str]:
        """Retorna el conjunto de variables que algún teorema puede calcular."""
        return set(self._index.keys())

    def __len__(self) -> int:
        return len(self._theorems)

    def __repr__(self) -> str:
        return f"KnowledgeBase({len(self)} teoremas, goals={sorted(self.known_goals())})"
