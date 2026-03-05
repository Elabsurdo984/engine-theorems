import math
import pytest
from core.knowledge import KnowledgeBase
from core.engine import InferenceEngine
from domains.geometry import AREA_CIRCULO, register


# ── Estructura del teorema ────────────────────────────────────────────────────

def test_tiene_dos_conclusiones():
    assert len(AREA_CIRCULO.conclusions) == 2


def test_puede_probar_area_y_radio():
    assert AREA_CIRCULO.can_prove("area")
    assert AREA_CIRCULO.can_prove("r")


def test_dominio_es_geometria():
    assert AREA_CIRCULO.domain == "geometria"


def test_unidad_area_es_m2():
    c = AREA_CIRCULO.conclusion_for("area")
    assert c.unit == "m^2"


def test_unidad_radio_es_m():
    c = AREA_CIRCULO.conclusion_for("r")
    assert c.unit == "m"


# ── Integración con el motor ──────────────────────────────────────────────────

def make_engine():
    kb = KnowledgeBase()
    register(kb)
    return InferenceEngine(kb)


def test_area_desde_radio():
    result = make_engine().prove("area", {"r": 1})
    assert result.success
    assert result.value == pytest.approx(math.pi)


def test_area_radio_5():
    result = make_engine().prove("area", {"r": 5})
    assert result.success
    assert result.value == pytest.approx(math.pi * 25)


def test_radio_desde_area():
    result = make_engine().prove("r", {"area": math.pi * 9})
    assert result.success
    assert result.value == pytest.approx(3.0)


def test_radio_desde_area_unitaria():
    result = make_engine().prove("r", {"area": math.pi})
    assert result.success
    assert result.value == pytest.approx(1.0)


def test_falla_con_radio_negativo():
    result = make_engine().prove("area", {"r": -2})
    assert not result.success


def test_falla_con_radio_cero():
    result = make_engine().prove("area", {"r": 0})
    assert not result.success


def test_falla_sin_datos():
    result = make_engine().prove("area", {})
    assert not result.success


def test_register_indexa_area_y_radio():
    kb = KnowledgeBase()
    register(kb)
    assert kb.theorems_for("area")
    assert kb.theorems_for("r")
