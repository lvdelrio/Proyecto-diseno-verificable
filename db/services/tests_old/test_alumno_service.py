import pytest
from unittest.mock import MagicMock, patch
from db.services.alumno_service import (
    get_available_cursos_con_secciones,
    register_alumno_in_secciones,
)

@patch("db.services.alumno_service.get_alumno_by_id")
@patch("db.services.alumno_service.get_all_cursos")
@patch("db.services.alumno_service.get_all_secciones_by_curso_id")
def test_get_available_cursos_con_secciones(mock_get_secciones, mock_get_cursos, mock_get_alumno):
    mock_get_alumno.return_value = MagicMock(secciones=[])
    mock_get_cursos.return_value = [MagicMock(id=1), MagicMock(id=2)]
    mock_get_secciones.side_effect = lambda db, curso_id: [MagicMock()] if curso_id == 1 else []
    db = MagicMock(session=MagicMock())

    alumno, cursos_with_secciones = get_available_cursos_con_secciones(db, 123)
    assert alumno is not None
    assert len(cursos_with_secciones) == 1

@patch("db.services.alumno_service.get_alumno_by_id")
@patch("db.services.alumno_service.get_all_cursos")
@patch("db.services.alumno_service.enroll_alumno_in_seccion")
def test_register_alumno_in_secciones(mock_enroll, mock_get_cursos, mock_get_alumno):
    mock_get_alumno.return_value = MagicMock()
    mock_get_cursos.return_value = [MagicMock(id=1, nombre="Curso1")]
    mock_enroll.return_value = (True, "Inscrito")
    db = MagicMock()
    form_data = {"seccion_id_1": "10"}
    alumno = register_alumno_in_secciones(db, 1, form_data)
    assert alumno is not None 


