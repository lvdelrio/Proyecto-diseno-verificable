import pytest
from unittest.mock import MagicMock, patch
from http import HTTPStatus
import unittest.mock

# Service tests
@patch("db.services.tipo_curso_service.get_tipo_curso_by_id")
@patch("db.services.tipo_curso_service.get_all_tipo_cursos")
def test_get_tipo_curso_and_cursos_disponibles(mock_get_all, mock_get_by_id, sample_tipo_curso):
    from db.services.tipo_curso_service import get_tipo_curso_and_cursos_disponibles
    
    mock_get_by_id.return_value = sample_tipo_curso
    
    mock_curso1 = MagicMock()
    mock_curso1.id = 2
    mock_curso2 = MagicMock()
    mock_curso2.id = 3
    mock_get_all.return_value = [mock_curso1, mock_curso2]
    
    mock_db = MagicMock()
    mock_db.session = MagicMock()
    
    tipo_curso, disponibles = get_tipo_curso_and_cursos_disponibles(mock_db, 1)
    
    assert tipo_curso is not None
    assert isinstance(disponibles, list)
    assert tipo_curso.codigo == "ICC1000"

@patch("db.services.tipo_curso_service.enroll_tipo_curso_in_tipo_cursos")
def test_register_tipo_curso_in_tipo_cursos_success(mock_enroll):
    from db.services.tipo_curso_service import register_tipo_curso_in_tipo_cursos
    
    mock_enroll.return_value = (True, "Requisito agregado exitosamente")
    
    mock_db = MagicMock()
    mock_form_data = MagicMock()
    mock_form_data.getlist.return_value = ["1", "2"]
    
    enrolled, errors = register_tipo_curso_in_tipo_cursos(mock_db, 1, mock_form_data)
    
    assert len(enrolled) == 2
    assert errors == []

@patch("db.services.tipo_curso_service.enroll_tipo_curso_in_tipo_cursos")
def test_register_tipo_curso_in_tipo_cursos_with_errors(mock_enroll):
    from db.services.tipo_curso_service import register_tipo_curso_in_tipo_cursos
    
    mock_enroll.side_effect = [(True, "Agregado"), (False, "Error al agregar")]
    
    mock_db = MagicMock()
    mock_form_data = MagicMock()
    mock_form_data.getlist.return_value = ["1", "2"]
    
    enrolled, errors = register_tipo_curso_in_tipo_cursos(mock_db, 1, mock_form_data)
    
    assert len(enrolled) == 1
    assert len(errors) == 1

# Controller tests
def test_create_tipo_curso():
    from db.controller.tipo_curso_controller import create_tipo_curso
    from db.models.tipo_curso import TipoCurso
    
    mock_db = MagicMock()
    
    result = create_tipo_curso(mock_db, "ICC1000", "Programación", 6)
    
    assert isinstance(result, TipoCurso)
    assert result.codigo == "ICC1000"
    assert result.descripcion == "Programación"
    assert result.creditos == 6
    
    mock_db.add.assert_called_once_with(result)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(result)

def test_create_tipo_curso_with_id():
    from db.controller.tipo_curso_controller import create_tipo_curso
    from db.models.tipo_curso import TipoCurso
    
    mock_db = MagicMock()
    
    result = create_tipo_curso(mock_db, "ICC2000", "Algoritmos", 8, tipo_curso_id=123)
    
    assert isinstance(result, TipoCurso)
    assert result.id == 123
    assert result.codigo == "ICC2000"

def test_get_tipo_curso_by_id():
    from db.controller.tipo_curso_controller import get_tipo_curso_by_id
    
    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_query
    
    result = get_tipo_curso_by_id(mock_db, 1)
    
    assert result == mock_query
    mock_db.query.assert_called_once()

def test_get_all_tipo_cursos():
    from db.controller.tipo_curso_controller import get_all_tipo_cursos
    
    mock_db = MagicMock()
    mock_tipos = [MagicMock(), MagicMock()]
    mock_db.query.return_value.all.return_value = mock_tipos
    
    result = get_all_tipo_cursos(mock_db)
    
    assert result == mock_tipos
    mock_db.query.assert_called_once()

@patch("db.controller.tipo_curso_controller.get_tipo_curso_by_id")
def test_edit_tipo_curso_by_id_success(mock_get_tipo_curso, sample_tipo_curso):
    from db.controller.tipo_curso_controller import edit_tipo_curso_by_id
    
    mock_get_tipo_curso.return_value = sample_tipo_curso
    mock_db = MagicMock()
    
    result = edit_tipo_curso_by_id(mock_db, 1, "ICC1001", "Nueva descripción")
    
    assert sample_tipo_curso.codigo == "ICC1001"
    assert sample_tipo_curso.descripcion == "Nueva descripción"
    mock_db.commit.assert_called_once()
    assert result == sample_tipo_curso

@patch("db.controller.tipo_curso_controller.get_tipo_curso_by_id")
def test_edit_tipo_curso_by_id_not_found(mock_get_tipo_curso):
    from db.controller.tipo_curso_controller import edit_tipo_curso_by_id
    
    mock_get_tipo_curso.return_value = None
    mock_db = MagicMock()
    
    result = edit_tipo_curso_by_id(mock_db, 999, "ICC999", "No existe")
    
    assert result is None
    mock_db.commit.assert_not_called()

@patch("db.controller.tipo_curso_controller.get_tipo_curso_by_id")
def test_delete_tipo_curso_by_id_success(mock_get_tipo_curso, sample_tipo_curso):
    from db.controller.tipo_curso_controller import delete_tipo_curso_by_id
    
    mock_get_tipo_curso.return_value = sample_tipo_curso
    mock_db = MagicMock()
    
    result = delete_tipo_curso_by_id(mock_db, 1)
    
    assert result is True
    mock_db.delete.assert_called_once_with(sample_tipo_curso)
    mock_db.commit.assert_called_once()

@patch("db.controller.tipo_curso_controller.get_tipo_curso_by_id")
def test_delete_tipo_curso_by_id_not_found(mock_get_tipo_curso):
    from db.controller.tipo_curso_controller import delete_tipo_curso_by_id
    
    mock_get_tipo_curso.return_value = None
    mock_db = MagicMock()
    
    result = delete_tipo_curso_by_id(mock_db, 999)
    
    assert result is False
    mock_db.delete.assert_not_called()

@patch("db.controller.tipo_curso_controller.validate_requisito_tipo_curso")
@patch("db.controller.tipo_curso_controller.create_requisito")
def test_enroll_tipo_curso_in_tipo_cursos_success(mock_create_req, mock_validate):
    from db.controller.tipo_curso_controller import enroll_tipo_curso_in_tipo_cursos
    
    mock_validate.return_value = None  # No existe el requisito
    mock_db = MagicMock()
    
    success, message = enroll_tipo_curso_in_tipo_cursos(mock_db, 1, 2)
    
    assert success is True
    assert "exitosamente" in message
    mock_create_req.assert_called_once()

def test_enroll_tipo_curso_in_tipo_cursos_same_id():
    from db.controller.tipo_curso_controller import enroll_tipo_curso_in_tipo_cursos
    
    mock_db = MagicMock()
    
    success, message = enroll_tipo_curso_in_tipo_cursos(mock_db, 1, 1)
    
    assert success is False
    assert "sí mismo" in message

@patch("db.controller.tipo_curso_controller.validate_requisito_tipo_curso")
def test_enroll_tipo_curso_in_tipo_cursos_already_exists(mock_validate):
    from db.controller.tipo_curso_controller import enroll_tipo_curso_in_tipo_cursos
    
    mock_validate.return_value = MagicMock()  # Ya existe
    mock_db = MagicMock()
    
    success, message = enroll_tipo_curso_in_tipo_cursos(mock_db, 1, 2)
    
    assert success is False
    assert "ya está asignado" in message

def test_validate_requisito_tipo_curso():
    from db.controller.tipo_curso_controller import validate_requisito_tipo_curso
    
    mock_db = MagicMock()
    mock_requisito = MagicMock()
    mock_db.query.return_value.filter_by.return_value.first.return_value = mock_requisito
    
    result = validate_requisito_tipo_curso(mock_db, 1, 2)
    
    assert result == mock_requisito
    mock_db.query.assert_called_once()

def test_create_requisito():
    from db.controller.tipo_curso_controller import create_requisito
    from db.models.requisitos import CursoRequisito
    
    mock_db = MagicMock()
    
    with patch("db.controller.tipo_curso_controller.CursoRequisito") as mock_requisito_class:
        mock_requisito = MagicMock()
        mock_requisito_class.return_value = mock_requisito
        
        result = create_requisito(mock_db, 1, 2)
        
        mock_requisito_class.assert_called_with(tipo_curso_id=1, curso_requisito_id=2)
        mock_db.add.assert_called_once_with(mock_requisito)
        mock_db.commit.assert_called_once()
        assert result == mock_requisito

@patch("db.controller.tipo_curso_controller.create_tipo_curso")
@patch("db.controller.tipo_curso_controller.enroll_tipo_curso_in_tipo_cursos")
def test_create_tipo_cursos_from_json(mock_enroll, mock_create):
    from db.controller.tipo_curso_controller import create_tipo_cursos_from_json
    
    mock_tipo_curso = MagicMock()
    mock_tipo_curso.id = 1
    mock_create.return_value = mock_tipo_curso
    
    data = {
        "cursos": [
            {
                "id": 1,
                "codigo": "ICC1000",
                "descripcion": "Programación",
                "creditos": 6,
                "requisitos": ["ICC2000"]
            },
            {
                "id": 2,
                "codigo": "ICC2000", 
                "descripcion": "Algoritmos",
                "creditos": 8,
                "requisitos": []
            }
        ]
    }
    
    mock_db = MagicMock()
    
    create_tipo_cursos_from_json(mock_db, data)
    
    assert mock_create.call_count == 2
    mock_enroll.assert_called_once()

# Routes tests
def test_get_tipo_cursos_route(client):
    with patch("routes.tipo_cursos_routes.get_all_tipo_cursos") as mock_get_all:
        mock_get_all.return_value = []
        
        response = client.get('/tipo_cursos')
        assert response.status_code == 200

def test_add_tipo_curso_route(client):
    with patch("routes.tipo_cursos_routes.create_tipo_curso") as mock_create:
        mock_tipo_curso = MagicMock()
        mock_tipo_curso.id = 1
        mock_create.return_value = mock_tipo_curso
        
        response = client.post('/agregar_tipo_curso', data={
            'codigo': 'ICC1000',
            'descripcion': 'Programación',
            'credits': '6'
        })
        assert response.status_code == 302  # Redirect

def test_edit_tipo_curso_route(client):
    with patch("routes.tipo_cursos_routes.edit_tipo_curso_by_id") as mock_edit:
        response = client.post('/editar_tipo_curso/1', data={
            'codigo': 'ICC1001',
            'descripcion': 'Nueva descripción'
        })
        assert response.status_code == 302  # Redirect
        mock_edit.assert_called_once()

def test_delete_tipo_curso_route(client):
    with patch("routes.tipo_cursos_routes.delete_tipo_curso_by_id") as mock_delete:
        response = client.post('/borrar_tipo_curso/1')
        assert response.status_code == 302  # Redirect
        mock_delete.assert_called_once_with(unittest.mock.ANY, 1)

def test_register_tipo_curso_route(client):
    with patch("routes.tipo_cursos_routes.register_tipo_curso_in_tipo_cursos") as mock_register:
        response = client.post('/inscribir_curso/1/', data={
            'tipo_curso_ids': ['2', '3']
        })
        assert response.status_code == 302  # Redirect
        mock_register.assert_called_once()

def test_load_tipo_cursos_route(client):
    with patch("routes.tipo_cursos_routes.create_tipo_cursos_from_json") as mock_create:
        data = {
            "cursos": [
                {"id": 1, "codigo": "ICC1000", "descripcion": "Test", "creditos": 6, "requisitos": []}
            ]
        }
        response = client.post('/importar_tipo_cursos',
                             json=data,
                             content_type='application/json')
        assert response.status_code == 201
        mock_create.assert_called_once()

# Model tests
def test_tipo_curso_model_creation():
    from db.models.tipo_curso import TipoCurso
    
    tipo_curso = TipoCurso(codigo="ICC1000", descripcion="Programación", creditos=6)
    assert tipo_curso.codigo == "ICC1000"
    assert tipo_curso.descripcion == "Programación"
    assert tipo_curso.creditos == 6

def test_tipo_curso_model_with_id():
    from db.models.tipo_curso import TipoCurso
    
    tipo_curso = TipoCurso(id=1, codigo="ICC2000", descripcion="Algoritmos", creditos=8)
    assert tipo_curso.id == 1
    assert tipo_curso.codigo == "ICC2000"

def test_tipo_curso_model_repr():
    from db.models.tipo_curso import TipoCurso
    
    tipo_curso = TipoCurso(id=1, codigo="ICC1000", descripcion="Test", creditos=6)
    repr_str = repr(tipo_curso)
    assert "Tipo de curso" in repr_str
    assert "1" in repr_str
    assert "ICC1000" in repr_str