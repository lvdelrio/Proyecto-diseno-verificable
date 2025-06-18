import pytest
from unittest.mock import MagicMock, patch
from http import HTTPStatus
from datetime import datetime
import unittest.mock

# Service tests
@patch("db.services.alumno_service.get_alumno_by_id")
@patch("db.services.alumno_service.get_all_cursos")
@patch("db.services.alumno_service.get_all_secciones_by_curso_id")
def test_get_available_cursos_con_secciones(mock_get_secciones, mock_get_cursos, mock_get_alumno, sample_alumno):
    from db.services.alumno_service import get_available_cursos_con_secciones
    
    mock_get_alumno.return_value = sample_alumno
    
    mock_curso = MagicMock()
    mock_curso.id = 1
    mock_get_cursos.return_value = [mock_curso]
    
    mock_seccion = MagicMock()
    mock_seccion.id = 1
    mock_get_secciones.return_value = [mock_seccion]
    
    mock_db = MagicMock()
    mock_db.session = MagicMock()
    
    alumno, cursos_with_secciones = get_available_cursos_con_secciones(mock_db, 1)
    
    assert alumno is not None
    assert isinstance(cursos_with_secciones, list)
    assert alumno.nombre == "Juan Estudiante"

@patch("db.services.alumno_service.get_alumno_by_id")
def test_get_available_cursos_con_secciones_not_found(mock_get_alumno):
    from db.services.alumno_service import get_available_cursos_con_secciones
    from flask import Flask
    
    mock_get_alumno.return_value = None
    mock_db = MagicMock()
    mock_db.session = MagicMock()
    
    app = Flask(__name__)
    with app.app_context():
        with pytest.raises(Exception):  # abort raises exception
            get_available_cursos_con_secciones(mock_db, 999)

@patch("db.services.alumno_service.get_alumno_by_id")
@patch("db.services.alumno_service.get_all_cursos")
@patch("db.services.alumno_service.enroll_alumno_in_seccion")
def test_register_alumno_in_secciones_success(mock_enroll, mock_get_cursos, mock_get_alumno, sample_alumno):
    from db.services.alumno_service import register_alumno_in_secciones
    
    mock_get_alumno.return_value = sample_alumno
    
    mock_curso = MagicMock()
    mock_curso.id = 1
    mock_curso.nombre = "Programación"
    mock_get_cursos.return_value = [mock_curso]
    
    mock_enroll.return_value = (True, "Inscrito exitosamente")
    
    mock_db = MagicMock()
    form_data = {"seccion_id_1": "10"}
    
    alumno = register_alumno_in_secciones(mock_db, 1, form_data)
    
    assert alumno is not None
    assert alumno.nombre == "Juan Estudiante"

@patch("db.services.alumno_service.get_alumno_by_id")
def test_register_alumno_in_secciones_not_found(mock_get_alumno):
    from db.services.alumno_service import register_alumno_in_secciones
    
    mock_get_alumno.return_value = None
    mock_db = MagicMock()
    form_data = {}
    
    result = register_alumno_in_secciones(mock_db, 999, form_data)
    
    assert result is None

# Controller tests
def test_create_alumno():
    from db.controller.alumno_controller import create_alumno
    from db.models.alumno import Alumno
    
    mock_db = MagicMock()
    
    result = create_alumno(mock_db, "Test Alumno", "test@email.com", "2024-01-01")
    
    assert isinstance(result, Alumno)
    assert result.nombre == "Test Alumno"
    assert result.email == "test@email.com"
    
    mock_db.add.assert_called_once_with(result)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(result)

def test_create_alumno_with_id():
    from db.controller.alumno_controller import create_alumno
    from db.models.alumno import Alumno
    
    mock_db = MagicMock()
    
    result = create_alumno(mock_db, "Test", "test@email.com", "2024-01-01", alumno_id=123)
    
    assert isinstance(result, Alumno)
    assert result.id == 123

def test_create_alumno_without_fecha():
    from db.controller.alumno_controller import create_alumno
    from db.models.alumno import Alumno
    
    mock_db = MagicMock()
    
    result = create_alumno(mock_db, "Test", "test@email.com")
    
    assert isinstance(result, Alumno)
    assert result.fecha_ingreso is None

def test_get_alumno_by_id():
    from db.controller.alumno_controller import get_alumno_by_id
    
    mock_db = MagicMock()
    mock_alumno = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_alumno
    
    result = get_alumno_by_id(mock_db, 1)
    
    assert result == mock_alumno
    mock_db.query.assert_called_once()

def test_get_all_alumnos():
    from db.controller.alumno_controller import get_all_alumnos
    
    mock_db = MagicMock()
    mock_alumnos = [MagicMock(), MagicMock()]
    mock_db.query.return_value.all.return_value = mock_alumnos
    
    result = get_all_alumnos(mock_db)
    
    assert result == mock_alumnos
    mock_db.query.assert_called_once()

@patch("db.controller.alumno_controller.get_alumno_by_id")
def test_edit_alumno_by_id_success(mock_get_alumno, sample_alumno):
    from db.controller.alumno_controller import edit_alumno_by_id
    
    mock_get_alumno.return_value = sample_alumno
    mock_db = MagicMock()
    
    result = edit_alumno_by_id(mock_db, 1, "Nuevo Nombre", "nuevo@email.com", "2024-06-01")
    
    assert sample_alumno.nombre == "Nuevo Nombre"
    assert sample_alumno.email == "nuevo@email.com"
    mock_db.commit.assert_called_once()
    assert result == sample_alumno

@patch("db.controller.alumno_controller.get_alumno_by_id")
def test_edit_alumno_by_id_not_found(mock_get_alumno):
    from db.controller.alumno_controller import edit_alumno_by_id
    
    mock_get_alumno.return_value = None
    mock_db = MagicMock()
    
    result = edit_alumno_by_id(mock_db, 999, "Nombre", "email@test.com")
    
    assert result is None
    mock_db.commit.assert_not_called()

@patch("db.controller.alumno_controller.get_alumno_by_id")
def test_delete_alumno_by_id_success(mock_get_alumno, sample_alumno):
    from db.controller.alumno_controller import delete_alumno_by_id
    
    mock_get_alumno.return_value = sample_alumno
    mock_db = MagicMock()
    
    result = delete_alumno_by_id(mock_db, 1)
    
    assert result is True
    mock_db.delete.assert_called_once_with(sample_alumno)
    mock_db.commit.assert_called_once()

@patch("db.controller.alumno_controller.get_alumno_by_id")
def test_delete_alumno_by_id_not_found(mock_get_alumno):
    from db.controller.alumno_controller import delete_alumno_by_id
    
    mock_get_alumno.return_value = None
    mock_db = MagicMock()
    
    result = delete_alumno_by_id(mock_db, 999)
    
    assert result is False
    mock_db.delete.assert_not_called()

def test_get_paginated_alumnos():
    from db.controller.alumno_controller import get_paginated_alumnos
    
    mock_session = MagicMock()
    mock_paginate = MagicMock()
    mock_session.query.return_value.order_by.return_value.paginate.return_value = mock_paginate
    
    result = get_paginated_alumnos(mock_session, page=2, per_page=5)
    
    mock_session.query.assert_called_once()
    assert result == mock_paginate

@patch("db.controller.alumno_controller.get_alumno_by_id")
@patch("db.controller.alumno_controller.get_seccion_by_id")
def test_enroll_alumno_in_seccion_success(mock_get_seccion, mock_get_alumno, sample_alumno):
    from db.controller.alumno_controller import enroll_alumno_in_seccion
    
    mock_seccion = MagicMock()
    mock_get_alumno.return_value = sample_alumno
    mock_get_seccion.return_value = mock_seccion
    
    mock_db = MagicMock()
    
    success, message = enroll_alumno_in_seccion(mock_db, 1, 1)
    
    assert success is True
    assert "exitosamente" in message
    assert mock_seccion in sample_alumno.secciones

@patch("db.controller.alumno_controller.get_alumno_by_id")
@patch("db.controller.alumno_controller.get_seccion_by_id")
def test_enroll_alumno_in_seccion_already_enrolled(mock_get_seccion, mock_get_alumno):
    from db.controller.alumno_controller import enroll_alumno_in_seccion
    from db.models.alumno import Alumno
    
    mock_seccion = MagicMock()
    alumno = Alumno(id=1, nombre="Test", email="test@email.com", fecha_ingreso=datetime.now().date())
    alumno.secciones = [mock_seccion]
    
    mock_get_alumno.return_value = alumno
    mock_get_seccion.return_value = mock_seccion
    
    mock_db = MagicMock()
    
    success, message = enroll_alumno_in_seccion(mock_db, 1, 1)
    
    assert success is False
    assert "ya está inscrito" in message

@patch("db.controller.alumno_controller.get_alumno_by_id")
@patch("db.controller.alumno_controller.get_seccion_by_id")
def test_unregister_alumno_in_seccion_success(mock_get_seccion, mock_get_alumno):
    from db.controller.alumno_controller import unregister_alumno_in_seccion
    from db.models.alumno import Alumno
    
    mock_seccion = MagicMock()
    alumno = Alumno(id=1, nombre="Test", email="test@email.com", fecha_ingreso=datetime.now().date())
    alumno.secciones = [mock_seccion]
    
    mock_get_alumno.return_value = alumno
    mock_get_seccion.return_value = mock_seccion
    
    mock_db = MagicMock()
    
    success, message = unregister_alumno_in_seccion(mock_db, 1, 1)
    
    assert success is True
    assert "removido" in message

@patch("db.controller.alumno_controller.get_alumno_by_id")
def test_unregister_alumno_in_seccion_alumno_not_found(mock_get_alumno):
    from db.controller.alumno_controller import unregister_alumno_in_seccion
    
    mock_get_alumno.return_value = None
    mock_db = MagicMock()
    
    success, message = unregister_alumno_in_seccion(mock_db, 999, 1)
    
    assert success is False
    assert "no encontrado" in message

@patch("db.controller.alumno_controller.create_alumno")
def test_create_alumnos_from_json(mock_create):
    from db.controller.alumno_controller import create_alumnos_from_json
    
    mock_alumno = MagicMock()
    mock_create.return_value = mock_alumno
    
    data = {
        "alumnos": [
            {"id": 1, "nombre": "Alumno 1", "correo": "alumno1@test.com", "anio_ingreso": 2024},
            {"id": 2, "nombre": "Alumno 2", "correo": "alumno2@test.com", "anio_ingreso": 2023}
        ]
    }
    
    mock_db = MagicMock()
    
    create_alumnos_from_json(mock_db, data)
    
    assert mock_create.call_count == 2

# Routes tests
def test_get_alumnos_route(client):
    with patch("routes.alumnos_routes.get_paginated_alumnos") as mock_paginated:
        mock_result = MagicMock()
        mock_result.items = []
        mock_result.pages = 1
        mock_result.total = 0
        mock_paginated.return_value = mock_result
        
        response = client.get('/alumnos')
        assert response.status_code == 200

def test_get_alumnos_route_with_page(client):
    with patch("routes.alumnos_routes.get_paginated_alumnos") as mock_paginated:
        mock_result = MagicMock()
        mock_result.items = []
        mock_result.pages = 1
        mock_result.total = 0
        mock_paginated.return_value = mock_result
        
        response = client.get('/alumnos/2')
        assert response.status_code == 200

def test_add_alumno_route(client):
    with patch("routes.alumnos_routes.create_alumno") as mock_create:
        mock_alumno = MagicMock()
        mock_alumno.id = 1
        mock_create.return_value = mock_alumno
        
        response = client.post('/agregar_alumno', data={
            'nombre': 'Test Alumno',
            'email': 'test@email.com',
            'fecha_ingreso': '2024-01-01'
        })
        assert response.status_code == 302  # Redirect

def test_edit_alumno_route(client):
    with patch("routes.alumnos_routes.edit_alumno_by_id") as mock_edit:
        response = client.post('/editar_alumno/1', data={
            'nombre': 'Nombre Editado',
            'email': 'editado@email.com',
            'fecha_ingreso': '2024-06-01'
        })
        assert response.status_code == 302  # Redirect
        mock_edit.assert_called_once()

def test_delete_alumno_route(client):
    with patch("routes.alumnos_routes.delete_alumno_by_id") as mock_delete:
        response = client.post('/borrar_alumno/1')
        assert response.status_code == 302  # Redirect
        mock_delete.assert_called_once_with(unittest.mock.ANY, 1)

def test_register_alumno_route(client):
    with patch("routes.alumnos_routes.register_alumno_in_secciones") as mock_register:
        mock_register.return_value = MagicMock()  # Return alumno object
        response = client.post('/inscribir_alumno/1/', data={
            'seccion_id_1': '10'
        })
        assert response.status_code == 302  # Redirect
        mock_register.assert_called_once()

def test_register_alumno_route_not_found(client):
    with patch("routes.alumnos_routes.register_alumno_in_secciones") as mock_register:
        mock_register.return_value = None
        response = client.post('/inscribir_alumno/999/')
        assert response.status_code == 404

def test_unregister_alumno_route(client):
    with patch("routes.alumnos_routes.unregister_alumno_in_seccion") as mock_unregister:
        response = client.post('/desinscribir_alumno/1/', data={
            'alumno_id': '1'
        })
        assert response.status_code == 302  # Redirect
        mock_unregister.assert_called_once()

def test_load_alumnos_route_success(client):
    with patch("routes.alumnos_routes.create_alumnos_from_json") as mock_create:
        mock_create.return_value = (True, "Alumnos cargados correctamente")
        data = {
            "alumnos": [
                {"id": 1, "nombre": "Test", "correo": "test@email.com", "anio_ingreso": 2024}
            ]
        }
        response = client.post('/importar_alumnos',
                             json=data,
                             content_type='application/json')
        assert response.status_code == 201
        mock_create.assert_called_once()

def test_load_alumnos_route_failure(client):
    with patch("routes.alumnos_routes.create_alumnos_from_json") as mock_create:
        mock_create.return_value = (False, "Error al cargar alumnos")
        data = {"alumnos": []}
        response = client.post('/importar_alumnos',
                             json=data,
                             content_type='application/json')
        assert response.status_code == 400

def test_alumno_model_creation():
    from db.models.alumno import Alumno
    
    fecha = datetime(2024, 1, 1)
    alumno = Alumno(nombre="Test Alumno", email="test@email.com", fecha_ingreso=fecha)
    assert alumno.nombre == "Test Alumno"
    assert alumno.email == "test@email.com"
    assert alumno.fecha_ingreso == fecha

def test_alumno_model_with_id():
    from db.models.alumno import Alumno
    
    alumno = Alumno(id=1, nombre="Test", email="test@email.com", fecha_ingreso=datetime.now())
    assert alumno.id == 1
    assert alumno.nombre == "Test"

def test_alumno_model_repr():
    from db.models.alumno import Alumno
    
    alumno = Alumno(id=1, nombre="Test Alumno", email="test@email.com", fecha_ingreso=datetime.now())
    repr_str = repr(alumno)
    assert "Alumno" in repr_str
    assert "1" in repr_str
    assert "Test Alumno" in repr_str