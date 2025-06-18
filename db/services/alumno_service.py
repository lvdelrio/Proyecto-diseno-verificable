from http import HTTPStatus
from flask import abort
from sqlalchemy.orm import Session
from db.controller.curso_controller import get_all_cursos
from db.controller.seccion_controller import get_all_secciones_by_curso_id
from db.controller.alumno_controller import enroll_alumno_in_seccion
from db.controller.common_controller import get_alumno_by_id

LISTA_VACIA = 0

def get_available_cursos_con_secciones(db, alumno_id):
    alumno = get_alumno_by_id(db.session, alumno_id)
    if alumno is None:
        abort(HTTPStatus.NOT_FOUND, description="Alumno no encontrado.")

    available_cursos = _get_available_cursos_for_alumno(db, alumno)
    cursos_with_secciones = _filter_cursos_with_secciones(db, available_cursos)

    return alumno, cursos_with_secciones

def _get_available_cursos_for_alumno(db, alumno):
    registered_cursos_ids = {seccion.curso_id for seccion in alumno.secciones}
    return [
        curso for curso in get_all_cursos(db.session)
        if curso.id not in registered_cursos_ids
    ]

def _filter_cursos_with_secciones(db, cursos):
    cursos_with_secciones = []
    for curso in cursos:
        secciones = get_all_secciones_by_curso_id(db.session, curso.id)
        if len(secciones) == LISTA_VACIA:
            continue
        cursos_with_secciones.append((curso, secciones))
    return cursos_with_secciones

def register_alumno_in_secciones(db, alumno_id, form_data):
    alumno = get_alumno_by_id(db, alumno_id)
    if not alumno:
        return None

    cursos = get_all_cursos(db)
    enrolled_sections, errors = _process_enrollment(db, alumno_id, cursos, form_data)

    return alumno

def _process_enrollment(db, alumno_id, cursos, form_data):
    enrolled_sections = []
    errors = []
    for curso in cursos:
        seccion_id = form_data.get(f'seccion_id_{curso.id}')
        if seccion_id:
            try:
                seccion_id_int = int(seccion_id)
                success, message = enroll_alumno_in_seccion(db, alumno_id, seccion_id_int)
                if success:
                    enrolled_sections.append(message)
                else:
                    errors.append(message)
            except ValueError:
                errors.append(f"ID inválido para la sección del curso {curso.nombre}")
    return enrolled_sections, errors
