import pytest
from core.knowledge import KnowledgeBase
from core.engine import InferenceEngine
from domains.physics import LEY_DE_NEWTON, register


# ── Estructura del teorema ────────────────────────────────────────────────────

def test_tiene_tres_conclusiones():
    assert len(LEY_DE_NEWTON.conclusions) == 3


def test_puede_probar_fuerza_masa_y_aceleracion():
    assert LEY_DE_NEWTON.can_prove("F")
    assert LEY_DE_NEWTON.can_prove("m")
    assert LEY_DE_NEWTON.can_prove("a")


def test_dominio_es_fisica():
    assert LEY_DE_NEWTON.domain == "fisica"


def test_unidades():
    assert LEY_DE_NEWTON.conclusion_for("F").unit == "N"
    assert LEY_DE_NEWTON.conclusion_for("m").unit == "kg"
    assert LEY_DE_NEWTON.conclusion_for("a").unit == "m/s^2"


# ── Integracion con el motor ──────────────────────────────────────────────────

def make_engine():
    kb = KnowledgeBase()
    register(kb)
    return InferenceEngine(kb)


def test_fuerza_desde_masa_y_aceleracion():
    result = make_engine().prove("F", {"m": 10, "a": 3})
    assert result.success
    assert result.value == pytest.approx(30.0)


def test_masa_desde_fuerza_y_aceleracion():
    result = make_engine().prove("m", {"F": 30, "a": 3})
    assert result.success
    assert result.value == pytest.approx(10.0)


def test_aceleracion_desde_fuerza_y_masa():
    result = make_engine().prove("a", {"F": 30, "m": 10})
    assert result.success
    assert result.value == pytest.approx(3.0)


def test_falla_con_masa_negativa():
    result = make_engine().prove("F", {"m": -5, "a": 3})
    assert not result.success


def test_falla_con_masa_cero():
    result = make_engine().prove("F", {"m": 0, "a": 3})
    assert not result.success


def test_falla_sin_datos():
    result = make_engine().prove("F", {})
    assert not result.success


# ── Encadenamiento con cinematica ─────────────────────────────────────────────
#
# El motor puede derivar 'a' desde Newton y usarla en cinematica
# automaticamente, sin que el usuario tenga que calcularlo.

def test_velocidad_final_con_fuerza_y_masa():
    # a = F/m = 20/4 = 5 m/s^2
    # v = v0 + a*t = 0 + 5*2 = 10 m/s
    result = make_engine().prove("v", {"F": 20, "m": 4, "v0": 0, "t": 2})
    assert result.success
    assert result.value == pytest.approx(10.0)


def test_desplazamiento_con_fuerza_y_masa():
    # a = F/m = 20/4 = 5 m/s^2
    # d = v0*t + a*t^2/2 = 0 + 5*4/2 = 10 m
    result = make_engine().prove("d", {"F": 20, "m": 4, "v0": 0, "t": 2})
    assert result.success
    assert result.value == pytest.approx(10.0)


def test_cadena_registra_dos_pasos():
    # Paso 1: Newton calcula 'a'. Paso 2: cinematica calcula 'v'.
    result = make_engine().prove("v", {"F": 20, "m": 4, "v0": 0, "t": 2})
    assert len(result.steps) == 2
