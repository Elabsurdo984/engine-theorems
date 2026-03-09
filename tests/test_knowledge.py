import pytest
from core.knowledge import KnowledgeBase
from core.theorem import Theorem, Hypothesis, Conclusion


# ── Fixtures ─────────────────────────────────────────────────────────────────

def make_theorem(name, domain, conclusions_vars):
    """Crea un teorema mínimo con las variables de conclusión indicadas."""
    return Theorem(
        name=name,
        domain=domain,
        description="",
        variables={},
        hypotheses=[],
        conclusions=[
            Conclusion(var, "0", f"produce {var}")
            for var in conclusions_vars
        ],
    )


def make_kb_with_pythagoras():
    kb = KnowledgeBase()
    theorem = Theorem(
        name="Teorema de Pitágoras",
        domain="geometría",
        description="c² = a² + b²",
        variables={"a": "cateto", "b": "cateto", "c": "hipotenusa"},
        hypotheses=[
            Hypothesis("a > 0"),
            Hypothesis("b > 0"),
        ],
        conclusions=[
            Conclusion("c", "sqrt(a**2 + b**2)", "hipotenusa dado a y b"),
            Conclusion("a", "sqrt(c**2 - b**2)", "cateto a dado c y b"),
            Conclusion("b", "sqrt(c**2 - a**2)", "cateto b dado c y a"),
        ],
    )
    kb.register(theorem)
    return kb, theorem


# ── register ─────────────────────────────────────────────────────────────────

def test_register_increases_count():
    kb = KnowledgeBase()
    assert len(kb) == 0
    kb.register(make_theorem("T1", "math", ["x"]))
    assert len(kb) == 1


def test_register_multiple_theorems():
    kb = KnowledgeBase()
    kb.register(make_theorem("T1", "math", ["x"]))
    kb.register(make_theorem("T2", "math", ["y"]))
    assert len(kb) == 2


# ── theorems_for ─────────────────────────────────────────────────────────────

def test_theorems_for_returns_correct_theorem():
    kb, theorem = make_kb_with_pythagoras()
    results = kb.theorems_for("c")
    assert theorem in results


def test_theorems_for_all_conclusions_are_indexed():
    kb, theorem = make_kb_with_pythagoras()
    assert theorem in kb.theorems_for("a")
    assert theorem in kb.theorems_for("b")
    assert theorem in kb.theorems_for("c")


def test_theorems_for_unknown_goal_returns_empty():
    kb, _ = make_kb_with_pythagoras()
    assert kb.theorems_for("z") == []


def test_two_theorems_can_prove_same_goal():
    kb = KnowledgeBase()
    t1 = make_theorem("T1", "math", ["x"])
    t2 = make_theorem("T2", "math", ["x"])
    kb.register(t1)
    kb.register(t2)
    results = kb.theorems_for("x")
    assert t1 in results
    assert t2 in results


# ── all_theorems / theorems_by_domain ────────────────────────────────────────

def test_all_theorems_returns_all():
    kb = KnowledgeBase()
    t1 = make_theorem("T1", "math", ["x"])
    t2 = make_theorem("T2", "physics", ["y"])
    kb.register(t1)
    kb.register(t2)
    all_t = kb.all_theorems()
    assert t1 in all_t and t2 in all_t and len(all_t) == 2


def test_theorems_by_domain_filters_correctly():
    kb = KnowledgeBase()
    kb.register(make_theorem("T1", "geometría", ["x"]))
    kb.register(make_theorem("T2", "álgebra", ["y"]))
    results = kb.theorems_by_domain("geometría")
    assert len(results) == 1
    assert results[0].name == "T1"


def test_theorems_by_domain_returns_empty_for_unknown_domain():
    kb, _ = make_kb_with_pythagoras()
    assert kb.theorems_by_domain("física cuántica") == []


# ── known_goals ───────────────────────────────────────────────────────────────

def test_known_goals_contains_all_indexed_variables():
    kb, _ = make_kb_with_pythagoras()
    assert kb.known_goals() == {"a", "b", "c"}
