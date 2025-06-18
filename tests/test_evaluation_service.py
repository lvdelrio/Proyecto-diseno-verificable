import pytest
from db.services.evalaution_service import get_evaluacion_by_instancia
from db.models.evaluacion import Evaluacion

@pytest.fixture
def evaluaciones_mock():
    return [
        Evaluacion(nombre="Evaluacion 2", ponderacion=0.3, opcional=0, tipo_ponderacion=True),
        Evaluacion(nombre="Evaluacion 1", ponderacion=0.3, opcional=0, tipo_ponderacion=True),
        Evaluacion(nombre="Evaluacion 3", ponderacion=0.4, opcional=1, tipo_ponderacion=False),
    ]

def test_get_evaluacion_by_instancia_orden_simple(evaluaciones_mock):
    result = get_evaluacion_by_instancia(evaluaciones_mock, 1)
    assert result.nombre == 'Evaluacion 1'

    result = get_evaluacion_by_instancia(evaluaciones_mock, 2)
    assert result.nombre == 'Evaluacion 2'

    result = get_evaluacion_by_instancia(evaluaciones_mock, 3)
    assert result.nombre == 'Evaluacion 3'

def test_get_evaluacion_by_instancia_out_of_range(evaluaciones_mock):
    with pytest.raises(IndexError):
        get_evaluacion_by_instancia(evaluaciones_mock, 4)
