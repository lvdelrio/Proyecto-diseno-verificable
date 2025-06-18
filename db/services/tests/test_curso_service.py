import pytest
from werkzeug.exceptions import NotFound
from unittest.mock import patch, MagicMock
from http import HTTPStatus
from db.services.curso_service import check_curso_cerrado

@patch("db.services.curso_service.get_curso_by_id")
@patch("db.services.curso_service.abort")
def test_check_curso_cerrado_not_found(mock_abort, mock_get_curso):
    mock_get_curso.return_value = None
    mock_abort.side_effect = NotFound("Curso no encontrado")

    db = MagicMock()
    curso_id = 1

    with pytest.raises(NotFound):
        check_curso_cerrado(db, curso_id)

    mock_abort.assert_called_once_with(HTTPStatus.NOT_FOUND, description="Curso no encontrado")

@patch("db.services.curso_service.get_curso_by_id")
@patch("db.services.curso_service.abort")
def test_check_curso_cerrado_cerrado(mock_abort, mock_get_curso):
    mock_get_curso.return_value = MagicMock(cerrado=True)
    db = MagicMock()
    curso_id = 2
    check_curso_cerrado(db, curso_id)
    mock_abort.assert_called_once_with(HTTPStatus.FORBIDDEN, description="El curso está cerrado y ya no se puede modificar")

@patch("db.services.curso_service.get_curso_by_id")
@patch("db.services.curso_service.abort")
def test_check_curso_cerrado_abierto(mock_abort, mock_get_curso):
    mock_get_curso.return_value = MagicMock(cerrado=False)
    db = MagicMock()
    curso_id = 3
    result = check_curso_cerrado(db, curso_id)
    mock_abort.assert_not_called()
    assert result is True 