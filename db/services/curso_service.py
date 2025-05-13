from flask import abort
from sqlalchemy.orm import Session
from ..controller.curso_controller import get_curso_by_id

def check_curso_cerrado(db: Session, curso_id=None):    
    curso = get_curso_by_id(db, curso_id)
    if not curso:
        abort(404, description="Curso no encontrado")
    
    if curso.cerrado:
        abort(403, description="El curso está cerrado y ya no se puede modificar")
    
    return True
