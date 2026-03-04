import pytest
from core.knowledge import KnowledgeBase
from core.engine import InferenceEngine
from domains.electricity import OHM, POTENCIA_VI, POTENCIA_IR, POTENCIA_VR, register

# Caso base: V=12V, I=2A, R=6Ohm, P=24W


def make_engine():
    kb = KnowledgeBase()
    register(kb)
    return InferenceEngine(kb)


# ── Ley de Ohm ────────────────────────────────────────────────────────────────

def test_calcula_tension():
    result = make_engine().prove("V", {"i": 2, "R": 6})
    assert result.success
    assert result.value == pytest.approx(12.0)


def test_calcula_corriente():
    result = make_engine().prove("i", {"V": 12, "R": 6})
    assert result.success
    assert result.value == pytest.approx(2.0)


def test_calcula_resistencia():
    result = make_engine().prove("R", {"V": 12, "i": 2})
    assert result.success
    assert result.value == pytest.approx(6.0)


# ── Potencia P = V * I ────────────────────────────────────────────────────────

def test_calcula_potencia_vi():
    result = make_engine().prove("P", {"V": 12, "i": 2})
    assert result.success
    assert result.value == pytest.approx(24.0)


def test_calcula_tension_desde_potencia_y_corriente():
    result = make_engine().prove("V", {"P": 24, "i": 2})
    assert result.success
    assert result.value == pytest.approx(12.0)


# ── Potencia P = I^2 * R ─────────────────────────────────────────────────────

def test_calcula_potencia_ir():
    result = make_engine().prove("P", {"i": 2, "R": 6})
    assert result.success
    assert result.value == pytest.approx(24.0)


def test_calcula_corriente_desde_potencia_y_resistencia():
    result = make_engine().prove("i", {"P": 24, "R": 6})
    assert result.success
    assert result.value == pytest.approx(2.0)


def test_calcula_resistencia_desde_potencia_y_corriente():
    result = make_engine().prove("R", {"P": 24, "i": 2})
    assert result.success
    assert result.value == pytest.approx(6.0)


# ── Potencia P = V^2 / R ─────────────────────────────────────────────────────

def test_calcula_potencia_vr():
    result = make_engine().prove("P", {"V": 12, "R": 6})
    assert result.success
    assert result.value == pytest.approx(24.0)


def test_calcula_tension_desde_potencia_y_resistencia():
    result = make_engine().prove("V", {"P": 24, "R": 6})
    assert result.success
    assert result.value == pytest.approx(12.0)


# ── Casos de fallo ────────────────────────────────────────────────────────────

def test_falla_con_resistencia_cero():
    result = make_engine().prove("V", {"i": 2, "R": 0})
    assert not result.success


def test_falla_con_datos_insuficientes():
    result = make_engine().prove("P", {"V": 12})
    assert not result.success
