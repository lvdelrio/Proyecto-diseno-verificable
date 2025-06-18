from http import HTTPStatus
from flask import abort
from sqlalchemy.orm import Session
from db.controller.tipo_curso_controller import (get_tipo_curso_by_id,
                                                 get_all_tipo_cursos,
                                                 enroll_tipo_curso_in_tipo_cursos)

def get_tipo_curso_and_cursos_disponibles(db, tipo_curso_id):
    tipo_curso_base = get_tipo_curso_by_id(db.session, tipo_curso_id)
    if tipo_curso_base is None:
        abort(HTTPStatus.NOT_FOUND, description="Tipo curso no encontrado.")

    cursos_disponibles = _get_cursos_disponibles_para_tipo_curso(db, tipo_curso_base, tipo_curso_id)
    return tipo_curso_base, cursos_disponibles

def _get_cursos_disponibles_para_tipo_curso(db, tipo_curso_base, tipo_curso_id):
    tipo_cursos_inscritos_ids = {
        requisito.curso_requisito.id
        for requisito in tipo_curso_base.requisitos
        if requisito.curso_requisito is not None
    }
    return [
        curso for curso in get_all_tipo_cursos(db.session)
        if curso.id not in tipo_cursos_inscritos_ids and curso.id != tipo_curso_id
    ]

def register_tipo_curso_in_tipo_cursos(db, tipo_curso_id, form_data):
    tipo_cursos_ids = [int(tipo_id) for tipo_id in form_data.getlist("tipo_curso_ids")]
    enrolled_tipo_cursos, errors = _process_tipo_curso_enrollment(db, tipo_curso_id, tipo_cursos_ids)
    return enrolled_tipo_cursos, errors


def _process_tipo_curso_enrollment(db, tipo_curso_id, tipo_cursos_ids):
    enrolled_tipo_cursos = []
    errors = []
    for tipo_id in tipo_cursos_ids:
        success, message = enroll_tipo_curso_in_tipo_cursos(db, tipo_curso_id, tipo_id)
        if success:
            enrolled_tipo_cursos.append(message)
        else:
            errors.append(message)
    return enrolled_tipo_cursos, errors
