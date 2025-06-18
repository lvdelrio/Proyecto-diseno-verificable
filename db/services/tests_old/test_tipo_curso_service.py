import pytest
from unittest.mock import MagicMock, patch
from db.services.tipo_curso_service import (
    get_tipo_curso_and_cursos_disponibles,
    register_tipo_curso_in_tipo_cursos,
)

@patch("db.services.tipo_curso_service.get_tipo_curso_by_id")
@patch("db.services.tipo_curso_service.get_all_tipo_cursos")
def test_get_tipo_curso_and_cursos_disponibles(mock_get_all, mock_get_by_id):
    tipo_curso = MagicMock()
    tipo_curso.requisitos = []
    mock_get_by_id.return_value = tipo_curso
    mock_get_all.return_value = [MagicMock(id=1), MagicMock(id=2)]
    db = MagicMock(session=MagicMock())

    base, disponibles = get_tipo_curso_and_cursos_disponibles(db, 1)
    assert base is not None
    assert isinstance(disponibles, list)

@patch("db.services.tipo_curso_service.enroll_tipo_curso_in_tipo_cursos")
def test_register_tipo_curso_in_tipo_cursos(mock_enroll):
    mock_enroll.return_value = (True, "Inscrito")
    db = MagicMock()
    form_data = MagicMock()
    form_data.getlist.return_value = ["1", "2"]
    enrolled, errors = register_tipo_curso_in_tipo_cursos(db, 1, form_data)
    assert len(enrolled) == 2
    assert errors == [] 