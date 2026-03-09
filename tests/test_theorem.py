from core.theorem import Hypothesis, Conclusion, Theorem


# ── Hypothesis ──────────────────────────────────────────────────────────────

def test_hypothesis_passes_when_condition_is_true():
    h = Hypothesis("a > 0")
    assert h.verify({"a": 5}) is True


def test_hypothesis_fails_when_condition_is_false():
    h = Hypothesis("a > 0")
    assert h.verify({"a": -3}) is False


def test_hypothesis_returns_none_on_missing_variable():
    h = Hypothesis("a > 0")
    assert h.verify({}) is None  # NameError → no se puede evaluar, diferir


def test_hypothesis_fails_gracefully_on_division_by_zero():
    h = Hypothesis("1/x > 0")
    assert h.verify({"x": 0}) is False


# ── Theorem ──────────────────────────────────────────────────────────────────

def make_pythagorean_theorem():
    return Theorem(
        name="Teorema de Pitágoras",
        domain="geometría",
        description="En un triángulo rectángulo: c² = a² + b²",
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


def test_can_prove_returns_true_for_known_goal():
    t = make_pythagorean_theorem()
    assert t.can_prove("c") is True
    assert t.can_prove("a") is True
    assert t.can_prove("b") is True


def test_can_prove_returns_false_for_unknown_goal():
    t = make_pythagorean_theorem()
    assert t.can_prove("x") is False


def test_conclusion_for_returns_correct_conclusion():
    t = make_pythagorean_theorem()
    c = t.conclusion_for("c")
    assert c is not None
    assert c.variable == "c"
    assert c.expression == "sqrt(a**2 + b**2)"


def test_conclusion_for_returns_none_when_not_found():
    t = make_pythagorean_theorem()
    assert t.conclusion_for("x") is None
