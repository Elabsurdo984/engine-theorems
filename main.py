from core.knowledge import KnowledgeBase
from ui.console import ConsoleApp
import domains.geometry as geometry


def build_knowledge_base() -> KnowledgeBase:
    """Construye y retorna la base de conocimiento con todos los dominios."""
    kb = KnowledgeBase()
    geometry.register(kb)
    return kb


def main() -> None:
    kb = build_knowledge_base()
    app = ConsoleApp(kb)
    app.run()


if __name__ == "__main__":
    main()
