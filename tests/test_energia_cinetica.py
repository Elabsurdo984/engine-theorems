import pytest
from core.knowledge import KnowledgeBase
from core.engine import InferenceEngine
from domains.physics import ENERGIA_CINETICA, register

# ── Estructura del teorema ────────────────────────────────────────────────────

def test_tiene_tres_conclusiones():
    assert len(ENERGIA_CINETICA.conclusions) == 3


def test_puede_probar_ec_masa_y_velocidad():
    assert ENERGIA_CINETICA.can_prove("Ec")
    assert ENERGIA_CINETICA.can_prove("m")
    assert ENERGIA_CINETICA.can_prove("v")


def test_dominio_es_fisica():
    assert ENERGIA_CINETICA.domain == "fisica"


def test_unidades():
    assert ENERGIA_CINETICA.conclusion_for("Ec").unit == "J"
    assert ENERGIA_CINETICA.conclusion_for("m").unit == "kg"
    assert ENERGIA_CINETICA.conclusion_for("v").unit == "m/s"


# ── Integracion con el motor ──────────────────────────────────────────────────

def make_engine():
    kb = KnowledgeBase()
    register(kb)
    return InferenceEngine(kb)


def test_energia_desde_masa_y_velocidad():
    result = make_engine().prove("Ec", {"m": 2, "v": 4})
    assert result.success
    assert result.value == pytest.approx(16.0)


def test_energia_con_velocidad_unitaria():
    result = make_engine().prove("Ec", {"m": 10, "v": 1})
    assert result.success
    assert result.value == pytest.approx(5.0)


def test_masa_desde_energia_y_velocidad():
    result = make_engine().prove("m", {"Ec": 16, "v": 4})
    assert result.success
    assert result.value == pytest.approx(2.0)


def test_velocidad_desde_energia_y_masa():
    result = make_engine().prove("v", {"Ec": 16, "m": 2})
    assert result.success
    assert result.value == pytest.approx(4.0)


def test_falla_con_masa_negativa():
    result = make_engine().prove("Ec", {"m": -2, "v": 4})
    assert not result.success


def test_falla_con_masa_cero():
    result = make_engine().prove("Ec", {"m": 0, "v": 4})
    assert not result.success


def test_falla_sin_datos():
    result = make_engine().prove("Ec", {})
    assert not result.success


# ── Encadenamiento con Newton ─────────────────────────────────────────────────
#
# Si se conocen F y m, el motor deriva 'a' con Newton,
# luego 'v' con cinematica, y finalmente 'Ec' con este teorema.

def test_energia_encadenada_desde_fuerza():
    # a = F/m = 20/4 = 5, v = v0 + a*t = 0 + 5*2 = 10
    # Ec = m*v^2/2 = 4*100/2 = 200 J
    result = make_engine().prove("Ec", {"F": 20, "m": 4, "v0": 0, "t": 2})
    assert result.success
    assert result.value == pytest.approx(200.0)


def test_cadena_registra_tres_pasos():
    # Paso 1: Newton → a, Paso 2: cinematica → v, Paso 3: Ec
    result = make_engine().prove("Ec", {"F": 20, "m": 4, "v0": 0, "t": 2})
    assert len(result.steps) == 3