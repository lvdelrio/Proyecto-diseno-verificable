import pytest
from unittest.mock import MagicMock
from app import app
from db.config import db

@pytest.fixture
def flask_app():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    return app

@pytest.fixture
def client(flask_app):
    return flask_app.test_client()

@pytest.fixture
def app_context(flask_app):
    with flask_app.app_context():
        yield flask_app

@pytest.fixture
def mock_db():
    mock_db = MagicMock()
    mock_db.session = MagicMock()
    return mock_db

@pytest.fixture
def sample_profesor():
    profesor = MagicMock()
    profesor.id = 1
    profesor.nombre = "Juan Perez"
    profesor.email = "juan@test.com"
    profesor.secciones = []
    return profesor

@pytest.fixture
def sample_tipo_curso():
    from db.models.tipo_curso import TipoCurso
    tipo_curso = TipoCurso(id=1, codigo="ICC1000", descripcion="Programación", creditos=6)
    tipo_curso.requisitos = []
    return tipo_curso

@pytest.fixture
def sample_alumno():
    from db.models.alumno import Alumno
    from datetime import datetime
    alumno = Alumno(id=1, nombre="Juan Estudiante", email="juan@estudiante.com", fecha_ingreso=datetime(2024, 1, 1))
    alumno.secciones = []
    return alumno
