from flask import abort
from sqlalchemy.orm import Session
from ..controller.curso_controller import get_all_cursos
from ..controller.seccion_controller import get_all_secciones_by_curso_id, get_seccion_by_id
from db.models.alumno import Alumno
from db.controller.alumno_controller import get_alumno_by_id, enroll_alumno_in_seccion
from utils.http_status import BAD_REQUEST, NOT_FOUND

def get_available_cursos_con_secciones(db: Session, alumno_id):
    alumno = get_alumno_by_id(db.session, alumno_id)

    if alumno is None:
        abort(NOT_FOUND, description="Alumno no encontrado.")

    registered_cursos_ids = {seccion.curso_id for seccion in alumno.secciones}

    available_cursos = [
        curso for curso in get_all_cursos(db.session)
        if curso.id not in registered_cursos_ids
    ]

    cursos_with_secciones = []
    for curso in available_cursos:
        secciones = get_all_secciones_by_curso_id(db.session, curso.id)
        if(len(secciones)==0): continue
        cursos_with_secciones.append((curso, secciones))

    return alumno, cursos_with_secciones

def register_alumno_in_secciones(db: Session, alumno_id: int, form_data: dict):
    alumno = get_alumno_by_id(db, alumno_id)
    if not alumno:
        return None

    cursos = get_all_cursos(db)
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

    return alumno
