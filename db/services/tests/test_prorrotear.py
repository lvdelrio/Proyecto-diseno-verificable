import pytest
from unittest.mock import MagicMock, patch
from db.utils.prorrotear import prorate_values, recalculate_categoria_ponderations, recalculate_seccion_ponderations

def test_prorate_values_normal():
    valores = [20.0, 30.0, 50.0]
    resultado = prorate_values(valores)
    assert resultado == [20.0, 30.0, 50.0]

def test_prorate_values_with_ajuste():
    valores = [10.0, 20.0, 30.0]
    resultado = prorate_values(valores)
    assert abs(sum(resultado) - 100.0) < 0.01
    assert len(resultado) == 3

def test_prorate_values_cero():
    valores = [0.0, 0.0, 0.0]
    resultado = prorate_values(valores)
    assert resultado == [0.0, 0.0, 0.0]

@patch('db.utils.prorrotear.get_evaluaciones_by_categoria_id')
def test_recalculate_categoria_ponderations_without_evaluaciones(mock_get_evaluaciones):
    mock_db = MagicMock()
    mock_get_evaluaciones.return_value = []   
    recalculate_categoria_ponderations(mock_db, 1)
    mock_db.commit.assert_not_called()

@patch('db.utils.prorrotear.get_evaluaciones_by_categoria_id')
def test_recalculate_categoria_ponderations_already_100(mock_get_evaluaciones):
    mock_db = MagicMock()
    mock_evaluacion1 = MagicMock(ponderacion=50.0)
    mock_evaluacion2 = MagicMock(ponderacion=50.0)
    mock_get_evaluaciones.return_value = [mock_evaluacion1, mock_evaluacion2]
    recalculate_categoria_ponderations(mock_db, 1)
    mock_db.commit.assert_not_called()

@patch('db.utils.prorrotear.get_evaluaciones_by_categoria_id')
def test_recalculate_categoria_ponderations_adjust(mock_get_evaluaciones):
    mock_db = MagicMock()
    mock_evaluacion1 = MagicMock(ponderacion=30.0)
    mock_evaluacion2 = MagicMock(ponderacion=30.0)
    mock_get_evaluaciones.return_value = [mock_evaluacion1, mock_evaluacion2]  
    recalculate_categoria_ponderations(mock_db, 1)
    mock_db.commit.assert_called_once()
    assert mock_evaluacion1.ponderacion == 50.0
    assert mock_evaluacion2.ponderacion == 50.0

@patch('db.utils.prorrotear.get_categorias_by_seccion_id')
def test_recalculate_seccion_ponderations_without_categorias(mock_get_categorias):
    mock_db = MagicMock()
    mock_get_categorias.return_value = []
    recalculate_seccion_ponderations(mock_db, 1)
    mock_db.commit.assert_not_called()

@patch('db.utils.prorrotear.get_categorias_by_seccion_id')
def test_recalculate_seccion_ponderations_adjust(mock_get_categorias):
    mock_db = MagicMock()
    mock_categoria1 = MagicMock(ponderacion=40.0)
    mock_categoria2 = MagicMock(ponderacion=40.0)
    mock_get_categorias.return_value = [mock_categoria1, mock_categoria2]   
    recalculate_seccion_ponderations(mock_db, 1)
    mock_db.commit.assert_called_once()
    assert mock_categoria1.ponderacion == 50.0
    assert mock_categoria2.ponderacion == 50.0