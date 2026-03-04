import pytest
from core.engine import InferenceEngine, ProofResult
from core.knowledge import KnowledgeBase
from core.theorem import Theorem, Hypothesis, Conclusion


# ── Helpers ───────────────────────────────────────────────────────────────────

def make_theorem(name, domain, conclusions: list[tuple], hypotheses=None):
    """
    conclusions: lista de (variable, expression_str, description)
    """
    return Theorem(
        name=name,
        domain=domain,
        description="",
        variables={},
        hypotheses=hypotheses or [],
        conclusions=[
            Conclusion(var, expr, desc)
            for var, expr, desc in conclusions
        ],
    )


def engine_with(*theorems):
    kb = KnowledgeBase()
    for t in theorems:
        kb.register(t)
    return InferenceEngine(kb)


# ── Prueba directa (Pitágoras) ────────────────────────────────────────────────

def pythagorean_theorem():
    return Theorem(
        name="Teorema de Pitágoras",
        domain="geometría",
        description="c² = a² + b²",
        variables={"a": "cateto", "b": "cateto", "c": "hipotenusa"},
        hypotheses=[
            Hypothesis("a > 0", lambda ctx: ctx["a"] > 0),
            Hypothesis("b > 0", lambda ctx: ctx["b"] > 0),
        ],
        conclusions=[
            Conclusion("c", "sqrt(a**2 + b**2)", "hipotenusa dado a y b"),
            Conclusion("a", "sqrt(c**2 - b**2)", "cateto a dado c y b"),
            Conclusion("b", "sqrt(c**2 - a**2)", "cateto b dado c y a"),
        ],
    )


def test_prove_hipotenusa_from_catetos():
    engine = engine_with(pythagorean_theorem())
    result = engine.prove("c", {"a": 3, "b": 4})
    assert result.success is True
    assert result.value == pytest.approx(5.0)


def test_prove_cateto_from_hipotenusa_and_other_cateto():
    engine = engine_with(pythagorean_theorem())
    result = engine.prove("a", {"c": 5, "b": 4})
    assert result.success is True
    assert result.value == pytest.approx(3.0)


def test_proof_records_theorem_name_in_steps():
    engine = engine_with(pythagorean_theorem())
    result = engine.prove("c", {"a": 3, "b": 4})
    assert result.steps[0].theorem_name == "Teorema de Pitágoras"


def test_proof_records_expression_in_steps():
    engine = engine_with(pythagorean_theorem())
    result = engine.prove("c", {"a": 3, "b": 4})
    assert result.steps[0].expression_str == "sqrt(a**2 + b**2)"


def test_proof_records_hypotheses_checked():
    engine = engine_with(pythagorean_theorem())
    result = engine.prove("c", {"a": 3, "b": 4})
    assert "a > 0" in result.steps[0].hypotheses_checked
    assert "b > 0" in result.steps[0].hypotheses_checked


# ── Objetivo ya conocido ──────────────────────────────────────────────────────

def test_goal_already_in_context_returns_immediately():
    engine = engine_with(pythagorean_theorem())
    result = engine.prove("c", {"a": 3, "b": 4, "c": 99})
    assert result.success is True
    assert result.value == pytest.approx(99.0)
    assert result.steps == []  # no se usó ningún teorema


# ── Hipótesis no satisfecha ───────────────────────────────────────────────────

def test_fails_when_hypothesis_not_satisfied():
    engine = engine_with(pythagorean_theorem())
    result = engine.prove("c", {"a": -1, "b": 4})  # a > 0 falla
    assert result.success is False
    assert result.value is None


# ── Sin teorema disponible ────────────────────────────────────────────────────

def test_fails_when_no_theorem_can_prove_goal():
    engine = engine_with(pythagorean_theorem())
    result = engine.prove("z", {"a": 3, "b": 4})
    assert result.success is False
    assert "z" in result.error


# ── Encadenamiento (backward chaining real) ───────────────────────────────────
#
# Escenario: queremos calcular `x`, pero para eso necesitamos `y`,
# que tampoco está dado — el motor debe probarlo primero.
#
# Teorema B: y = z + 1      (necesita z)
# Teorema A: x = y * 2      (necesita y)
# Dado: z = 4
# Esperado: y = 5, x = 10

def test_chained_proof_derives_intermediate_variable():
    theorem_b = make_theorem("Teorema B", "test", [("y", "z + 1", "y desde z")])
    theorem_a = make_theorem("Teorema A", "test", [("x", "y * 2", "x desde y")])

    engine = engine_with(theorem_b, theorem_a)
    result = engine.prove("x", {"z": 4})

    assert result.success is True
    assert result.value == pytest.approx(10.0)


def test_chained_proof_records_both_steps():
    theorem_b = make_theorem("Teorema B", "test", [("y", "z + 1", "y desde z")])
    theorem_a = make_theorem("Teorema A", "test", [("x", "y * 2", "x desde y")])

    engine = engine_with(theorem_b, theorem_a)
    result = engine.prove("x", {"z": 4})

    goals_proved = [s.goal for s in result.steps]
    assert "y" in goals_proved  # paso intermedio registrado
    assert "x" in goals_proved  # paso final registrado


# ── known no se modifica ──────────────────────────────────────────────────────

def test_prove_does_not_mutate_known_dict():
    engine = engine_with(pythagorean_theorem())
    known = {"a": 3, "b": 4}
    engine.prove("c", known)
    assert known == {"a": 3, "b": 4}  # sin modificaciones
