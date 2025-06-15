from http import HTTPStatus
from flask import abort
from sqlalchemy.orm import Session
from db.controller.curso_controller import get_curso_by_id

def check_curso_cerrado(db: Session, curso_id=None):
    curso = get_curso_by_id(db, curso_id)
    if not curso:
        abort(HTTPStatus.NOT_FOUND, description="Curso no encontrado")
    if curso.cerrado:
        abort(HTTPStatus.FORBIDDEN, description="El curso está cerrado y ya no se puede modificar")
    return True
