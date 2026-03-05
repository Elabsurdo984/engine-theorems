"""
Tests para ui/console.py

Estrategia:
  - mock de builtins.input para simular las elecciones del usuario
  - capsys de pytest para capturar stdout
  - KnowledgeBase minima con un teorema simple para aislar la UI de la logica
"""
import pytest
from unittest.mock import patch

from core.knowledge import KnowledgeBase
from core.theorem import Theorem, Hypothesis, Conclusion
from ui.console import ConsoleApp


# ── Fixtures ──────────────────────────────────────────────────────────────────

def _make_kb() -> KnowledgeBase:
    """Base de conocimiento minima con un teorema de prueba."""
    kb = KnowledgeBase()
    kb.register(Theorem(
        name="Doble",
        domain="matematica",
        description="y = 2 * x",
        variables={"x": "valor de entrada", "y": "doble de x"},
        hypotheses=[
            Hypothesis("x > 0", lambda ctx: ctx["x"] > 0),
        ],
        conclusions=[
            Conclusion("y", "2 * x", "doble", unit="u"),
            Conclusion("x", "y / 2", "mitad", unit="u"),
        ],
    ))
    return kb


@pytest.fixture
def app() -> ConsoleApp:
    return ConsoleApp(_make_kb())


@pytest.fixture
def theorem():
    return _make_kb().all_theorems()[0]


# ── _pick ─────────────────────────────────────────────────────────────────────

class TestPick:
    def test_valid_choice_returns_int(self, app):
        with patch("builtins.input", return_value="2"):
            assert app._pick("Elige", 3) == 2

    def test_first_choice(self, app):
        with patch("builtins.input", return_value="1"):
            assert app._pick("Elige", 3) == 1

    def test_last_choice(self, app):
        with patch("builtins.input", return_value="3"):
            assert app._pick("Elige", 3) == 3

    def test_empty_input_cancels(self, app):
        with patch("builtins.input", return_value=""):
            assert app._pick("Elige", 3) is None

    def test_out_of_range_retries(self, app, capsys):
        with patch("builtins.input", side_effect=["5", "1"]):
            result = app._pick("Elige", 3)
        assert result == 1
        assert "1 y 3" in capsys.readouterr().out

    def test_non_numeric_retries(self, app, capsys):
        with patch("builtins.input", side_effect=["abc", "2"]):
            result = app._pick("Elige", 3)
        assert result == 2
        assert "no es un numero valido" in capsys.readouterr().out

    def test_multiple_invalid_then_valid(self, app):
        with patch("builtins.input", side_effect=["0", "abc", "", "2"]):
            # 0 fuera de rango, abc invalido, "" cancela
            result = app._pick("Elige", 3)
        assert result is None  # "" cancela antes de llegar a "2"


# ── _select_domain ────────────────────────────────────────────────────────────

class TestSelectDomain:
    def test_returns_domain_name(self, app):
        with patch("builtins.input", return_value="1"):
            assert app._select_domain() == "matematica"

    def test_cancel_returns_none(self, app):
        with patch("builtins.input", return_value=""):
            assert app._select_domain() is None

    def test_prints_available_domains(self, app, capsys):
        with patch("builtins.input", return_value="1"):
            app._select_domain()
        out = capsys.readouterr().out
        assert "Dominios disponibles" in out
        assert "Matematica" in out

    def test_domains_sorted_alphabetically(self):
        kb = KnowledgeBase()
        for domain in ("zeta", "alfa", "beta"):
            kb.register(Theorem(
                name=domain, domain=domain, description="",
                variables={}, hypotheses=[],
                conclusions=[Conclusion("x", "1", "x")],
            ))
        app = ConsoleApp(kb)
        with patch("builtins.input", return_value="1"):
            assert app._select_domain() == "alfa"


# ── _select_theorem ───────────────────────────────────────────────────────────

class TestSelectTheorem:
    def test_returns_theorem_object(self, app):
        with patch("builtins.input", return_value="1"):
            t = app._select_theorem("matematica")
        assert t.name == "Doble"

    def test_cancel_returns_none(self, app):
        with patch("builtins.input", return_value=""):
            assert app._select_theorem("matematica") is None

    def test_prints_theorem_name_and_description(self, app, capsys):
        with patch("builtins.input", return_value="1"):
            app._select_theorem("matematica")
        out = capsys.readouterr().out
        assert "Doble" in out
        assert "y = 2 * x" in out


# ── _select_goal ──────────────────────────────────────────────────────────────

class TestSelectGoal:
    def test_returns_first_variable(self, app, theorem):
        with patch("builtins.input", return_value="1"):
            assert app._select_goal(theorem) == "y"

    def test_returns_second_variable(self, app, theorem):
        with patch("builtins.input", return_value="2"):
            assert app._select_goal(theorem) == "x"

    def test_cancel_returns_none(self, app, theorem):
        with patch("builtins.input", return_value=""):
            assert app._select_goal(theorem) is None

    def test_prints_variable_descriptions(self, app, theorem, capsys):
        with patch("builtins.input", return_value="1"):
            app._select_goal(theorem)
        out = capsys.readouterr().out
        assert "valor de entrada" in out
        assert "doble de x" in out

    def test_prints_theorem_name(self, app, theorem, capsys):
        with patch("builtins.input", return_value="1"):
            app._select_goal(theorem)
        assert "Doble" in capsys.readouterr().out


# ── _ask_inputs ───────────────────────────────────────────────────────────────

class TestAskInputs:
    def test_returns_required_variables(self, app, theorem):
        with patch("builtins.input", return_value="5"):
            known = app._ask_inputs(theorem, "y")
        assert known == {"x": 5.0}

    def test_integer_input(self, app, theorem):
        with patch("builtins.input", return_value="3"):
            known = app._ask_inputs(theorem, "y")
        assert known["x"] == pytest.approx(3.0)

    def test_float_with_period(self, app, theorem):
        with patch("builtins.input", return_value="3.14"):
            known = app._ask_inputs(theorem, "y")
        assert known["x"] == pytest.approx(3.14)

    def test_comma_as_decimal_separator(self, app, theorem):
        with patch("builtins.input", return_value="3,14"):
            known = app._ask_inputs(theorem, "y")
        assert known["x"] == pytest.approx(3.14)

    def test_invalid_input_retries(self, app, theorem, capsys):
        with patch("builtins.input", side_effect=["abc", "7"]):
            known = app._ask_inputs(theorem, "y")
        assert known == {"x": 7.0}
        assert "no es un numero valido" in capsys.readouterr().out

    def test_asks_for_different_var_depending_on_goal(self, app, theorem):
        # goal="x" usa expresion "y / 2", asi que pide "y"
        with patch("builtins.input", return_value="10"):
            known = app._ask_inputs(theorem, "x")
        assert known == {"y": 10.0}

    def test_prints_required_variable_list(self, app, theorem, capsys):
        with patch("builtins.input", return_value="5"):
            app._ask_inputs(theorem, "y")
        out = capsys.readouterr().out
        assert "calcular 'y'" in out
        assert "x" in out


# ── _session ──────────────────────────────────────────────────────────────────

class TestSession:
    def test_full_session_shows_result(self, app, capsys):
        # dominio=1, teorema=1, goal=1 (y), x=3 → y=6
        with patch("builtins.input", side_effect=["1", "1", "1", "3"]):
            app._session()
        out = capsys.readouterr().out
        assert "y = 6 u" in out

    def test_result_shows_unit(self, app, capsys):
        with patch("builtins.input", side_effect=["1", "1", "1", "4"]):
            app._session()
        assert " u" in capsys.readouterr().out

    def test_cancel_at_domain_skips_session(self, app, capsys):
        with patch("builtins.input", return_value=""):
            app._session()
        assert "Resultado" not in capsys.readouterr().out

    def test_cancel_at_theorem_skips_session(self, app, capsys):
        with patch("builtins.input", side_effect=["1", ""]):
            app._session()
        assert "Resultado" not in capsys.readouterr().out

    def test_cancel_at_goal_skips_session(self, app, capsys):
        with patch("builtins.input", side_effect=["1", "1", ""]):
            app._session()
        assert "Resultado" not in capsys.readouterr().out

    def test_second_goal_direction(self, app, capsys):
        # goal=2 (x), y=10 → x=5
        with patch("builtins.input", side_effect=["1", "1", "2", "10"]):
            app._session()
        assert "x = 5 u" in capsys.readouterr().out


# ── run ───────────────────────────────────────────────────────────────────────

class TestRun:
    def test_prints_welcome_banner(self, app, capsys):
        with patch("builtins.input", side_effect=["1", "1", "1", "3", "n"]):
            app.run()
        assert "Motor de Teoremas" in capsys.readouterr().out

    def test_one_session_then_quit(self, app, capsys):
        with patch("builtins.input", side_effect=["1", "1", "1", "3", "n"]):
            app.run()
        out = capsys.readouterr().out
        assert "y = 6 u" in out
        assert "Hasta luego" in out

    def test_two_sessions(self, app, capsys):
        # Sesion 1: y con x=3 → y=6
        # Sesion 2: x con y=10 → x=5
        with patch("builtins.input", side_effect=[
            "1", "1", "1", "3", "s",
            "1", "1", "2", "10", "n",
        ]):
            app.run()
        out = capsys.readouterr().out
        assert "y = 6 u" in out
        assert "x = 5 u" in out

    def test_keyboard_interrupt_exits_cleanly(self, app, capsys):
        with patch("builtins.input", side_effect=KeyboardInterrupt):
            app.run()
        assert "Hasta luego" in capsys.readouterr().out

    def test_answer_no_exits_after_first_session(self, app, capsys):
        with patch("builtins.input", side_effect=["1", "1", "1", "3", "n"]):
            app.run()
        # Solo una sesion
        out = capsys.readouterr().out
        assert out.count("Resultado final") == 1
