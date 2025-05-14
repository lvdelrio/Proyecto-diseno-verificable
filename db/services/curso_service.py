from flask import abort
from sqlalchemy.orm import Session
from ..controller.curso_controller import get_curso_by_id
from utils.http_status import BAD_REQUEST, NOT_FOUND, FORBIDDEN

def check_curso_cerrado(db: Session, curso_id=None):    
    curso = get_curso_by_id(db, curso_id)
    if not curso:
        abort(NOT_FOUND, description="Curso no encontrado")
    
    if curso.cerrado:
        abort(FORBIDDEN, description="El curso está cerrado y ya no se puede modificar")
    
    return True
