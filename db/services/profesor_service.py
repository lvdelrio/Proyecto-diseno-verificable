from http import HTTPStatus
from flask import abort
from sqlalchemy.orm import Session
from db.controller.curso_controller import get_all_cursos
from db.controller.seccion_controller import get_all_secciones_by_curso_id
from db.controller.common_controller import get_profesor_by_id
from db.controller.profesor_controller import enroll_profesor_in_seccion

def get_profesor_and_available_cursos_with_secciones(db, profesor_id):
    profesor = get_profesor_by_id(db.session, profesor_id)
    if profesor is None:
        abort(HTTPStatus.NOT_FOUND, description="Profesor no encontrado.")

    available_cursos = _get_available_cursos_with_secciones_for_profesor(db, profesor)
    return profesor, available_cursos

def _get_available_cursos_with_secciones_for_profesor(db, profesor):
    profesor_seccion_ids = {seccion.id for seccion in profesor.secciones}
    cursos_with_secciones = []
    for curso in get_all_cursos(db.session):
        available_secciones = [
            seccion for seccion in get_all_secciones_by_curso_id(db.session, curso.id)
            if seccion.id not in profesor_seccion_ids
        ]
        if available_secciones:
            cursos_with_secciones.append((curso, available_secciones))
    return cursos_with_secciones

def register_profesor_in_seccion(db, profesor_id, form_data):
    seccion_ids = [int(sid) for sid in form_data.getlist("seccion_ids")]
    enrolled_sections, errors = _process_profesor_enrollment(db, profesor_id, seccion_ids)
    return enrolled_sections, errors

def _process_profesor_enrollment(db, profesor_id, seccion_ids):
    enrolled_sections = []
    errors = []
    for seccion_id in seccion_ids:
        success, message = enroll_profesor_in_seccion(db, profesor_id, seccion_id)
        if success:
            enrolled_sections.append(message)
        else:
            errors.append(message)
    return enrolled_sections, errors
