import pytest
from unittest.mock import MagicMock, patch
from db.services.profesor_service import register_profesor_in_seccion

@patch("db.services.profesor_service.enroll_profesor_in_seccion")
def test_register_profesor_in_seccion_success(mock_enroll):
    mock_enroll.side_effect = [(True, "Inscrito en 1"), (True, "Inscrito en 2")]

    db = MagicMock()
    form_data = MagicMock()
    form_data.getlist.return_value = ["1", "2"]  # input como lista de strings

    enrolled, errors = register_profesor_in_seccion(db, 1, form_data)

    assert enrolled == ["Inscrito en 1", "Inscrito en 2"]
    assert errors == []

@patch("db.services.profesor_service.enroll_profesor_in_seccion")
def test_register_profesor_in_seccion_partial_failure(mock_enroll):
    mock_enroll.side_effect = [(True, "Inscrito en 1"), (False, "Ya está inscrito")]

    db = MagicMock()
    form_data = MagicMock()
    form_data.getlist.return_value = ["1", "2"]

    enrolled, errors = register_profesor_in_seccion(db, 1, form_data)

    assert enrolled == ["Inscrito en 1"]
    assert errors == ["Ya está inscrito"]

@patch("db.services.profesor_service.enroll_profesor_in_seccion")
def test_register_profesor_in_seccion_all_fail(mock_enroll):
    mock_enroll.side_effect = [(False, "Error en 1"), (False, "Error en 2")]

    db = MagicMock()
    form_data = MagicMock()
    form_data.getlist.return_value = ["1", "2"]

    enrolled, errors = register_profesor_in_seccion(db, 1, form_data)

    assert enrolled == []
    assert errors == ["Error en 1", "Error en 2"]
