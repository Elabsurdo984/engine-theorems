import pytest
from core.knowledge import KnowledgeBase
from core.engine import InferenceEngine
from domains.geometry import PITAGORAS, register


# ── Estructura del teorema ────────────────────────────────────────────────────

def test_pitagoras_tiene_tres_conclusiones():
    assert len(PITAGORAS.conclusions) == 3


def test_pitagoras_puede_probar_los_tres_lados():
    assert PITAGORAS.can_prove("a")
    assert PITAGORAS.can_prove("b")
    assert PITAGORAS.can_prove("c")


def test_pitagoras_dominio_es_geometria():
    assert PITAGORAS.domain == "geometria"


# ── register() ────────────────────────────────────────────────────────────────

def test_register_agrega_teoremas_al_kb():
    kb = KnowledgeBase()
    register(kb)
    assert len(kb) >= 1


def test_register_indexa_los_tres_lados():
    kb = KnowledgeBase()
    register(kb)
    assert kb.theorems_for("a")
    assert kb.theorems_for("b")
    assert kb.theorems_for("c")


# ── Integración con el motor ──────────────────────────────────────────────────

def make_engine():
    kb = KnowledgeBase()
    register(kb)
    return InferenceEngine(kb)


def test_calcula_hipotenusa_3_4_5():
    result = make_engine().prove("c", {"a": 3, "b": 4})
    assert result.success
    assert result.value == pytest.approx(5.0)


def test_calcula_cateto_desde_hipotenusa():
    result = make_engine().prove("a", {"c": 5, "b": 4})
    assert result.success
    assert result.value == pytest.approx(3.0)


def test_calcula_cateto_b_desde_hipotenusa():
    result = make_engine().prove("b", {"c": 5, "a": 3})
    assert result.success
    assert result.value == pytest.approx(4.0)


def test_falla_con_datos_insuficientes():
    result = make_engine().prove("c", {"a": 3})
    assert not result.success


def test_falla_con_valores_negativos():
    result = make_engine().prove("c", {"a": -3, "b": 4})
    assert not result.success
