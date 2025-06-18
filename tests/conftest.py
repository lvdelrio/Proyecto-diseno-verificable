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