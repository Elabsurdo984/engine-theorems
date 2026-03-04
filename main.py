from core.knowledge import KnowledgeBase
from ui.console import ConsoleApp
import domains.geometry as geometry
import domains.physics as physics
import domains.electricity as electricity


def build_knowledge_base() -> KnowledgeBase:
    """Construye y retorna la base de conocimiento con todos los dominios."""
    kb = KnowledgeBase()
    geometry.register(kb)
    physics.register(kb)
    electricity.register(kb)
    return kb


def main() -> None:
    kb = build_knowledge_base()
    app = ConsoleApp(kb)
    app.run()


if __name__ == "__main__":
    main()
