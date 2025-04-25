from flask import abort
from sqlalchemy.orm import Session
from ..controller.tipo_curso_controller import get_tipo_curso_by_id, get_all_tipo_cursos, enroll_tipo_curso_in_tipo_cursos

def get_tipo_curso_and_cursos_disponibles(db: Session, tipo_curso_id: int):
    tipo_curso_base = get_tipo_curso_by_id(db.session, tipo_curso_id)

    if tipo_curso_base is None:
        abort(404, description="Tipo curso no encontrado.")

    tipo_cursos_inscritos_ids = {
        requisito.curso_requisito.id
        for requisito in tipo_curso_base.requisitos
        if requisito.curso_requisito is not None
    }
    cursos_disponibles = [
        curso for curso in get_all_tipo_cursos(db.session)
        if curso.id not in tipo_cursos_inscritos_ids and curso.id != tipo_curso_id
    ]

    return tipo_curso_base, cursos_disponibles

def register_tipo_curso_in_tipo_cursos(db: Session, tipo_curso_id: int, form_data: dict):
    tipo_curso_by_id = get_tipo_curso_by_id(db.session, tipo_curso_id)
    tipo_cursos_ids = form_data.getlist("tipo_curso_ids")

    enrolled_tipo_cursos = []
    errors = []

    for tipo_id in tipo_cursos_ids:
        exito, mensaje = enroll_tipo_curso_in_tipo_cursos(db.session, tipo_curso_id, int(tipo_id))
        if exito:
            enrolled_tipo_cursos.append(mensaje)
        else:
            errors.append(mensaje)