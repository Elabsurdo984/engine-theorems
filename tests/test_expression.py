import pytest
from core.expression import Expression, ExpressionError


# ── Constructor ──────────────────────────────────────────────────────────────

def test_valid_expression_is_created():
    e = Expression("sqrt(a**2 + b**2)")
    assert repr(e) == "Expression('sqrt(a**2 + b**2)')"


def test_invalid_expression_raises_error():
    with pytest.raises(ExpressionError):
        Expression("sqrt(((")


# ── required_variables ───────────────────────────────────────────────────────

def test_required_variables_detected_correctly():
    e = Expression("sqrt(a**2 + b**2)")
    assert e.required_variables == {"a", "b"}


def test_constant_expression_has_no_variables():
    e = Expression("3**2 + 4**2")
    assert e.required_variables == set()


# ── can_evaluate ─────────────────────────────────────────────────────────────

def test_can_evaluate_with_full_context():
    e = Expression("sqrt(a**2 + b**2)")
    assert e.can_evaluate({"a": 3, "b": 4}) is True


def test_cannot_evaluate_with_missing_variable():
    e = Expression("sqrt(a**2 + b**2)")
    assert e.can_evaluate({"a": 3}) is False


def test_can_evaluate_ignores_extra_variables_in_context():
    e = Expression("a + b")
    assert e.can_evaluate({"a": 1, "b": 2, "c": 99}) is True


# ── evaluate ─────────────────────────────────────────────────────────────────

def test_evaluate_pythagorean_theorem():
    e = Expression("sqrt(a**2 + b**2)")
    assert e.evaluate({"a": 3, "b": 4}) == pytest.approx(5.0)


def test_evaluate_raises_error_when_variable_missing():
    e = Expression("sqrt(a**2 + b**2)")
    with pytest.raises(ExpressionError, match="Variables faltantes"):
        e.evaluate({"a": 3})


def test_evaluate_constant_expression():
    e = Expression("2 + 2")
    assert e.evaluate({}) == pytest.approx(4.0)


# ── solve_for ────────────────────────────────────────────────────────────────

def test_solve_for_cateto_given_hipotenusa_and_other_cateto():
    # sqrt(a**2 + b**2) = 5, b=4 → a=3
    e = Expression("sqrt(a**2 + b**2)")
    solutions = e.solve_for("a", value=5, context={"b": 4})
    assert pytest.approx(3.0) in solutions


def test_solve_for_returns_only_real_solutions():
    e = Expression("a**2 + 1")  # a**2 + 1 = 0 → no soluciones reales
    solutions = e.solve_for("a", value=0)
    assert solutions == []
