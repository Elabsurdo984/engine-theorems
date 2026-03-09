from core.engine import InferenceEngine, ProofResult
from core.explainer import Explainer, _format_number, _substitute
from core.knowledge import KnowledgeBase
from core.theorem import Theorem, Hypothesis, Conclusion


# ── Helpers ───────────────────────────────────────────────────────────────────

def make_engine():
    kb = KnowledgeBase()
    kb.register(Theorem(
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
    ))
    return InferenceEngine(kb)


# ── _format_number ────────────────────────────────────────────────────────────

def test_format_number_integer():
    assert _format_number(5.0) == "5"


def test_format_number_float():
    result = _format_number(3.1416)
    assert "3,14" in result


# ── _substitute ───────────────────────────────────────────────────────────────

def test_substitute_replaces_variables():
    result = _substitute("a + b", {"a": 3, "b": 4})
    assert result == "7"


def test_substitute_partial_context():
    result = _substitute("a + b", {"a": 3})
    assert "3" in result
    assert "b" in result


# ── Explainer.explain — éxito ─────────────────────────────────────────────────

def test_explain_contains_goal():
    engine = make_engine()
    result = engine.prove("c", {"a": 3, "b": 4})
    output = Explainer().explain(result, {"a": 3, "b": 4})
    assert "c" in output


def test_explain_contains_theorem_name():
    engine = make_engine()
    result = engine.prove("c", {"a": 3, "b": 4})
    output = Explainer().explain(result, {"a": 3, "b": 4})
    assert "Teorema de Pitágoras" in output


def test_explain_contains_formula():
    engine = make_engine()
    result = engine.prove("c", {"a": 3, "b": 4})
    output = Explainer().explain(result, {"a": 3, "b": 4})
    assert "sqrt(a**2 + b**2)" in output


def test_explain_contains_numeric_result():
    engine = make_engine()
    result = engine.prove("c", {"a": 3, "b": 4})
    output = Explainer().explain(result, {"a": 3, "b": 4})
    assert "5" in output


def test_explain_contains_hypotheses():
    engine = make_engine()
    result = engine.prove("c", {"a": 3, "b": 4})
    output = Explainer().explain(result, {"a": 3, "b": 4})
    assert "a > 0" in output
    assert "b > 0" in output


# ── Explainer.explain — fallo ─────────────────────────────────────────────────

def test_explain_failure_shows_error():
    engine = make_engine()
    result = engine.prove("z", {"a": 3, "b": 4})
    output = Explainer().explain(result, {"a": 3, "b": 4})
    assert "z" in output
    assert "[ERROR]" in output
