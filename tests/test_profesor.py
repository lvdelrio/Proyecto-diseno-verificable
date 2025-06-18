import pytest
import unittest
from unittest.mock import MagicMock, patch
from http import HTTPStatus
from flask import Flask

@patch("db.services.profesor_service.get_profesor_by_id")
@patch("db.services.profesor_service.get_all_cursos")
@patch("db.services.profesor_service.get_all_secciones_by_curso_id")
def test_get_profesor_and_available_cursos_with_secciones(mock_get_secciones, mock_get_cursos, mock_get_profesor, sample_profesor):
    from db.services.profesor_service import get_profesor_and_available_cursos_with_secciones
    
    mock_get_profesor.return_value = sample_profesor
    
    mock_curso = MagicMock()
    mock_curso.id = 1
    mock_get_cursos.return_value = [mock_curso]
    
    mock_seccion = MagicMock()
    mock_seccion.id = 1
    mock_get_secciones.return_value = [mock_seccion]
    
    mock_db = MagicMock()
    mock_db.session = MagicMock()
    
    profesor, cursos = get_profesor_and_available_cursos_with_secciones(mock_db, 1)
    
    assert profesor is not None
    assert isinstance(cursos, list)
    assert profesor.nombre == "Juan Perez"

@patch("db.services.profesor_service.enroll_profesor_in_seccion")
def test_register_profesor_in_seccion_success(mock_enroll):
    from db.services.profesor_service import register_profesor_in_seccion
    
    mock_enroll.return_value = (True, "Inscrito exitosamente")
    
    mock_db = MagicMock()
    mock_form_data = MagicMock()
    mock_form_data.getlist.return_value = ["1", "2"]
    
    enrolled, errors = register_profesor_in_seccion(mock_db, 1, mock_form_data)
    
    assert len(enrolled) == 2
    assert errors == []

@patch("db.services.profesor_service.enroll_profesor_in_seccion")
def test_register_profesor_in_seccion_with_errors(mock_enroll):
    from db.services.profesor_service import register_profesor_in_seccion
    
    mock_enroll.side_effect = [(True, "Inscrito"), (False, "Error al inscribir")]
    
    mock_db = MagicMock()
    mock_form_data = MagicMock()
    mock_form_data.getlist.return_value = ["1", "2"]
    
    enrolled, errors = register_profesor_in_seccion(mock_db, 1, mock_form_data)
    
    assert len(enrolled) == 1
    assert len(errors) == 1

# Controller tests
def test_create_profesor():
    from db.controller.profesor_controller import create_profesor
    from db.models.profesor import Profesor
    
    mock_db = MagicMock()
    
    with patch.object(Profesor, '__init__', return_value=None) as mock_init:
        with patch.object(mock_db, 'add') as mock_add:
            with patch.object(mock_db, 'commit') as mock_commit:
                with patch.object(mock_db, 'refresh') as mock_refresh:
                    
                    create_profesor(mock_db, "Test Profesor", "test@email.com")
                    
                    mock_init.assert_called_with(nombre="Test Profesor", email="test@email.com")
                    mock_add.assert_called_once()
                    mock_commit.assert_called_once()
                    mock_refresh.assert_called_once()

def test_create_profesor_with_id():
    from db.controller.profesor_controller import create_profesor
    
    mock_db = MagicMock()
    mock_profesor = MagicMock()
    
    with patch("db.controller.profesor_controller.Profesor") as mock_profesor_class:
        mock_profesor_class.return_value = mock_profesor
        
        result = create_profesor(mock_db, "Test", "test@email.com", profesor_id=123)
        
        mock_profesor_class.assert_called_with(id=123, nombre="Test", email="test@email.com")
        assert result == mock_profesor

@patch("db.controller.profesor_controller.get_profesor_by_id")
def test_edit_profesor_by_id_success(mock_get_profesor):
    from db.controller.profesor_controller import edit_profesor_by_id
    
    mock_profesor = MagicMock()
    mock_get_profesor.return_value = mock_profesor
    mock_db = MagicMock()
    
    result = edit_profesor_by_id(mock_db, 1, "Nuevo Nombre", "nuevo@email.com")
    
    assert mock_profesor.nombre == "Nuevo Nombre"
    assert mock_profesor.email == "nuevo@email.com"
    mock_db.commit.assert_called_once()
    assert result == mock_profesor

@patch("db.controller.profesor_controller.get_profesor_by_id")
def test_edit_profesor_by_id_not_found(mock_get_profesor):
    from db.controller.profesor_controller import edit_profesor_by_id
    
    mock_get_profesor.return_value = None
    mock_db = MagicMock()
    
    result = edit_profesor_by_id(mock_db, 999, "Nombre", "email@test.com")
    
    assert result is None
    mock_db.commit.assert_not_called()

@patch("db.controller.profesor_controller.get_profesor_by_id")
def test_delete_profesor_by_id_success(mock_get_profesor):
    from db.controller.profesor_controller import delete_profesor_by_id
    
    mock_profesor = MagicMock()
    mock_get_profesor.return_value = mock_profesor
    mock_db = MagicMock()
    
    result = delete_profesor_by_id(mock_db, 1)
    
    assert result is True
    mock_db.delete.assert_called_once_with(mock_profesor)
    mock_db.commit.assert_called_once()

@patch("db.controller.profesor_controller.get_profesor_by_id")
def test_delete_profesor_by_id_not_found(mock_get_profesor):
    from db.controller.profesor_controller import delete_profesor_by_id
    
    mock_get_profesor.return_value = None
    mock_db = MagicMock()
    
    result = delete_profesor_by_id(mock_db, 999)
    
    assert result is False
    mock_db.delete.assert_not_called()

def test_get_paginated_profesores():
    from db.controller.profesor_controller import get_paginated_profesores
    
    mock_session = MagicMock()
    mock_query = MagicMock()
    mock_paginate = MagicMock()
    mock_session.query.return_value.order_by.return_value.paginate.return_value = mock_paginate
    
    result = get_paginated_profesores(mock_session, page=2, per_page=5)
    
    mock_session.query.assert_called_once()
    assert result == mock_paginate

@patch("db.controller.profesor_controller.get_profesor_by_id")
@patch("db.controller.profesor_controller.get_seccion_by_id")
def test_enroll_profesor_in_seccion_success(mock_get_seccion, mock_get_profesor):
    from db.controller.profesor_controller import enroll_profesor_in_seccion
    
    mock_profesor = MagicMock()
    mock_profesor.secciones = []
    mock_seccion = MagicMock()
    
    mock_get_profesor.return_value = mock_profesor
    mock_get_seccion.return_value = mock_seccion
    
    mock_db = MagicMock()
    
    success, message = enroll_profesor_in_seccion(mock_db, 1, 1)
    
    assert success is True
    assert "exitosamente" in message
    assert mock_seccion in mock_profesor.secciones

@patch("db.controller.profesor_controller.get_profesor_by_id")
def test_enroll_profesor_in_seccion_profesor_not_found(mock_get_profesor):
    from db.controller.profesor_controller import enroll_profesor_in_seccion
    
    mock_get_profesor.return_value = None
    mock_db = MagicMock()
    
    success, message = enroll_profesor_in_seccion(mock_db, 999, 1)
    
    assert success is False
    assert "no encontrado" in message

@patch("db.controller.profesor_controller.get_profesor_by_id")
@patch("db.controller.profesor_controller.get_seccion_by_id")
def test_enroll_profesor_in_seccion_already_enrolled(mock_get_seccion, mock_get_profesor):
    from db.controller.profesor_controller import enroll_profesor_in_seccion
    
    mock_seccion = MagicMock()
    mock_profesor = MagicMock()
    mock_profesor.secciones = [mock_seccion]
    
    mock_get_profesor.return_value = mock_profesor
    mock_get_seccion.return_value = mock_seccion
    
    mock_db = MagicMock()
    
    success, message = enroll_profesor_in_seccion(mock_db, 1, 1)
    
    assert success is False
    assert "ya está inscrito" in message

def test_create_profesores_from_json():
    from db.controller.profesor_controller import create_profesores_from_json
    
    mock_db = MagicMock()
    data = {
        "profesores": [
            {"id": 1, "nombre": "Prof 1", "correo": "prof1@test.com"},
            {"id": 2, "nombre": "Prof 2", "correo": "prof2@test.com"}
        ]
    }
    
    with patch("db.controller.profesor_controller.create_profesor") as mock_create:
        create_profesores_from_json(mock_db, data)
        assert mock_create.call_count == 2

def test_get_profesores_route(client):
    with patch("routes.profesores_routes.get_paginated_profesores") as mock_paginated:
        mock_result = MagicMock()
        mock_result.items = []
        mock_result.pages = 1
        mock_result.total = 0
        mock_paginated.return_value = mock_result
        
        response = client.get('/profesores')
        assert response.status_code == 200

def test_add_profesor_route(client):
    with patch("routes.profesores_routes.create_profesor") as mock_create:
        mock_profesor = MagicMock()
        mock_profesor.id = 1
        mock_create.return_value = mock_profesor
        
        response = client.post('/agregar_profesor', data={
            'nombre': 'Test Profesor',
            'email': 'test@email.com'
        })
        assert response.status_code == 302  # Redirect

def test_edit_profesor_route(client):
    with patch("routes.profesores_routes.edit_profesor_by_id") as mock_edit:
        response = client.post('/editar_profesor/1', data={
            'nombre': 'Nombre Editado',
            'email': 'editado@email.com'
        })
        assert response.status_code == 302  # Redirect
        mock_edit.assert_called_once()

def test_delete_profesor_route(client):
    with patch("routes.profesores_routes.delete_profesor_by_id") as mock_delete:
        response = client.post('/borrar_profesor/1')
        assert response.status_code == 302  # Redirect
        mock_delete.assert_called_once_with(unittest.mock.ANY, 1)

def test_load_profesores_route(client):
    with patch("routes.profesores_routes.create_profesores_from_json") as mock_create:
        data = {"profesores": [{"id": 1, "nombre": "Test", "correo": "test@email.com"}]}
        response = client.post('/importar_profesores',
                             json=data,
                             content_type='application/json')
        assert response.status_code == 201
        mock_create.assert_called_once()
