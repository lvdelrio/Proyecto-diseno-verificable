from http import HTTPStatus
from flask import abort
from sqlalchemy.orm import Session
from db.controller.curso_controller import get_all_cursos
from db.controller.seccion_controller import get_all_secciones_by_curso_id
from db.controller.common_controller import get_profesor_by_id
from db.controller.profesor_controller import enroll_profesor_in_seccion

def get_profesor_and_available_cursos_with_secciones(db: Session, profesor_id: int):
    profesor = get_profesor_by_id(db.session, profesor_id)
    if profesor is None:
        abort(HTTPStatus.NOT_FOUND, description="Profesor no encontrado.")

    profesor_seccion_ids = {seccion.id for seccion in profesor.secciones}

    cursos_with_secciones = []
    for curso in get_all_cursos(db.session):
        available_secciones = [
            seccion for seccion in get_all_secciones_by_curso_id(db.session, curso.id)
            if seccion.id not in profesor_seccion_ids
        ]

        if available_secciones:
            cursos_with_secciones.append((curso, available_secciones))
    return profesor, cursos_with_secciones

def register_profesor_in_seccion(db: Session, profesor_id: int, form_data: dict):

    seccion_ids = int(form_data.getlist("seccion_ids"))
    enrolled_sections = []
    errors = []
    #seccion_ids es una lista de ids en int.
    for seccion_id in seccion_ids:
        success, message = enroll_profesor_in_seccion(db, profesor_id, seccion_ids)
        if success:
            enrolled_sections.append(message)
        else:
            errors.append(message)
