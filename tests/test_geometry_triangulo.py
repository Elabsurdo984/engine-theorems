import pytest
from core.knowledge import KnowledgeBase
from core.engine import InferenceEngine
from domains.geometry import AREA_TRIANGULO, register


# ── Estructura del teorema ────────────────────────────────────────────────────

def test_tiene_tres_conclusiones():
    assert len(AREA_TRIANGULO.conclusions) == 3


def test_puede_probar_area_base_y_altura():
    assert AREA_TRIANGULO.can_prove("area")
    assert AREA_TRIANGULO.can_prove("base")
    assert AREA_TRIANGULO.can_prove("altura")


def test_dominio_es_geometria():
    assert AREA_TRIANGULO.domain == "geometria"


def test_unidades():
    assert AREA_TRIANGULO.conclusion_for("area").unit == "m^2"
    assert AREA_TRIANGULO.conclusion_for("base").unit == "m"
    assert AREA_TRIANGULO.conclusion_for("altura").unit == "m"


# ── Integracion con el motor ──────────────────────────────────────────────────

def make_engine():
    kb = KnowledgeBase()
    register(kb)
    return InferenceEngine(kb)


def test_area_desde_base_y_altura():
    result = make_engine().prove("area", {"base": 6, "altura": 4})
    assert result.success
    assert result.value == pytest.approx(12.0)


def test_area_triangulo_rectangulo_3_4():
    result = make_engine().prove("area", {"base": 3, "altura": 4})
    assert result.success
    assert result.value == pytest.approx(6.0)


def test_base_desde_area_y_altura():
    result = make_engine().prove("base", {"area": 12, "altura": 4})
    assert result.success
    assert result.value == pytest.approx(6.0)


def test_altura_desde_area_y_base():
    result = make_engine().prove("altura", {"area": 12, "base": 6})
    assert result.success
    assert result.value == pytest.approx(4.0)


def test_falla_con_base_negativa():
    result = make_engine().prove("area", {"base": -3, "altura": 4})
    assert not result.success


def test_falla_con_altura_cero():
    result = make_engine().prove("area", {"base": 3, "altura": 0})
    assert not result.success


def test_falla_sin_datos():
    result = make_engine().prove("area", {})
    assert not result.success


def test_falla_con_solo_base():
    result = make_engine().prove("area", {"base": 5})
    assert not result.success


# ── Convivencia con AREA_CIRCULO ──────────────────────────────────────────────
#
# Ambos teoremas usan la variable 'area'. El motor debe elegir el correcto
# segun los datos disponibles.

def test_datos_de_triangulo_usan_area_triangulo():
    result = make_engine().prove("area", {"base": 6, "altura": 4})
    assert result.success
    assert result.value == pytest.approx(12.0)
    assert result.steps[0].theorem_name == "Area del triangulo"


def test_datos_de_circulo_usan_area_circulo():
    import math
    result = make_engine().prove("area", {"r": 1})
    assert result.success
    assert result.value == pytest.approx(math.pi)
    assert result.steps[0].theorem_name == "Area del circulo"
