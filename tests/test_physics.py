import pytest
from core.knowledge import KnowledgeBase
from core.engine import InferenceEngine
from domains.physics import (
    CINEMATICA_VT, CINEMATICA_DT, CINEMATICA_VD, CINEMATICA_DM, register
)

# Caso base: v0=0, a=2, t=5 → v=10, d=25
# Caso 2:   v0=10, v=30, t=4 → a=5, d=80


def make_engine():
    kb = KnowledgeBase()
    register(kb)
    return InferenceEngine(kb)


# ── Ecuacion 1: v = v0 + a*t ─────────────────────────────────────────────────

def test_calcula_velocidad_final():
    result = make_engine().prove("v", {"v0": 0, "a": 2, "t": 5})
    assert result.success
    assert result.value == pytest.approx(10.0)


def test_calcula_velocidad_inicial():
    result = make_engine().prove("v0", {"v": 10, "a": 2, "t": 5})
    assert result.success
    assert result.value == pytest.approx(0.0)


def test_calcula_aceleracion_vt():
    result = make_engine().prove("a", {"v0": 10, "v": 30, "t": 4})
    assert result.success
    assert result.value == pytest.approx(5.0)


def test_calcula_tiempo_vt():
    result = make_engine().prove("t", {"v0": 0, "v": 10, "a": 2})
    assert result.success
    assert result.value == pytest.approx(5.0)


# ── Ecuacion 2: d = v0*t + a*t^2/2 ──────────────────────────────────────────

def test_calcula_desplazamiento_dt():
    result = make_engine().prove("d", {"v0": 0, "a": 2, "t": 5})
    assert result.success
    assert result.value == pytest.approx(25.0)


def test_calcula_aceleracion_dt():
    result = make_engine().prove("a", {"d": 25, "v0": 0, "t": 5})
    assert result.success
    assert result.value == pytest.approx(2.0)


def test_calcula_v0_dt():
    result = make_engine().prove("v0", {"d": 25, "a": 2, "t": 5})
    assert result.success
    assert result.value == pytest.approx(0.0)


# ── Ecuacion 3: v^2 = v0^2 + 2*a*d ──────────────────────────────────────────

def test_calcula_velocidad_final_vd():
    result = make_engine().prove("v", {"v0": 0, "a": 2, "d": 25})
    assert result.success
    assert result.value == pytest.approx(10.0)


def test_calcula_desplazamiento_vd():
    result = make_engine().prove("d", {"v0": 0, "v": 10, "a": 2})
    assert result.success
    assert result.value == pytest.approx(25.0)


def test_calcula_aceleracion_vd():
    result = make_engine().prove("a", {"v0": 0, "v": 10, "d": 25})
    assert result.success
    assert result.value == pytest.approx(2.0)


# ── Ecuacion 4: d = (v0+v)*t/2 ───────────────────────────────────────────────

def test_calcula_desplazamiento_dm():
    result = make_engine().prove("d", {"v0": 10, "v": 30, "t": 4})
    assert result.success
    assert result.value == pytest.approx(80.0)


def test_calcula_tiempo_dm():
    result = make_engine().prove("t", {"v0": 10, "v": 30, "d": 80})
    assert result.success
    assert result.value == pytest.approx(4.0)


# ── Casos de fallo ────────────────────────────────────────────────────────────

def test_falla_con_datos_insuficientes():
    result = make_engine().prove("v", {"v0": 0})
    assert not result.success


def test_falla_con_t_cero():
    result = make_engine().prove("a", {"v0": 0, "v": 10, "t": 0})
    assert not result.success
