import math
import pytest
from core.knowledge import KnowledgeBase
from core.engine import InferenceEngine
from domains.geometry import LEY_DE_COSENOS, register


def make_engine():
    kb = KnowledgeBase()
    register(kb)
    return InferenceEngine(kb)


# ── Estructura ────────────────────────────────────────────────────────────────

def test_tiene_seis_conclusiones():
    assert len(LEY_DE_COSENOS.conclusions) == 6


def test_puede_probar_los_tres_lados_y_tres_angulos():
    for var in ("a", "b", "c", "A", "B", "C"):
        assert LEY_DE_COSENOS.can_prove(var)


# ── Calcular un lado ──────────────────────────────────────────────────────────
#
# Triangulo con a=5, b=7, C=60° (pi/3)
# c² = 25 + 49 - 2·5·7·cos(60°) = 74 - 35 = 39  →  c ≈ 6,245

def test_calcula_lado_c_dado_a_b_y_angulo_C():
    result = make_engine().prove("c", {"a": 5, "b": 7, "C": math.pi / 3})
    assert result.success
    assert result.value == pytest.approx(math.sqrt(39), rel=1e-4)


def test_calcula_lado_a_dado_b_c_y_angulo_A():
    # Triangulo equilatero: a=b=c=5, todos los angulos = pi/3
    result = make_engine().prove("a", {"b": 5, "c": 5, "A": math.pi / 3})
    assert result.success
    assert result.value == pytest.approx(5.0, rel=1e-4)


# ── Calcular un angulo ────────────────────────────────────────────────────────
#
# Triangulo 3-4-5: es rectangulo, el angulo C opuesto a la hipotenusa = pi/2

def test_calcula_angulo_C_en_triangulo_rectangulo():
    result = make_engine().prove("C", {"a": 3, "b": 4, "c": 5})
    assert result.success
    assert result.value == pytest.approx(math.pi / 2, rel=1e-4)


def test_calcula_angulo_en_triangulo_equilatero():
    # Todos los angulos = 60° = pi/3
    result = make_engine().prove("A", {"a": 5, "b": 5, "c": 5})
    assert result.success
    assert result.value == pytest.approx(math.pi / 3, rel=1e-4)


# ── Pitagoras sigue funcionando (regresion) ───────────────────────────────────

def test_pitagoras_no_es_afectado():
    result = make_engine().prove("c", {"a": 3, "b": 4})
    assert result.success
    assert result.value == pytest.approx(5.0)


# ── Casos de fallo ────────────────────────────────────────────────────────────

def test_falla_si_angulo_es_cero():
    result = make_engine().prove("c", {"a": 5, "b": 7, "C": 0})
    assert not result.success


def test_falla_si_faltan_datos():
    result = make_engine().prove("c", {"a": 5, "C": math.pi / 3})
    assert not result.success
