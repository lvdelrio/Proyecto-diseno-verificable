from datetime import datetime
from sqlalchemy.orm import Session
from db.models.alumno import Alumno
from db.controller.common_controller import get_seccion_by_id
from db.services.curso_service import check_curso_cerrado
from db.utils.json_validator import validate_json

def create_alumno(db: Session, name: str, email: str,
                fecha_ingreso: str = None, alumno_id: int = None):
    fecha_ingreso_dt=datetime.strptime(fecha_ingreso, '%Y-%m-%d').date() if fecha_ingreso else None
    if alumno_id is not None:
        new_user = Alumno(id=alumno_id, nombre=name, email=email, fecha_ingreso=fecha_ingreso_dt)
    else:
        new_user = Alumno(nombre=name, email=email, fecha_ingreso=fecha_ingreso_dt)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_alumno_by_id(db: Session, user_id: int):
    return db.query(Alumno).filter(Alumno.id == user_id).first()

def get_all_alumnos(db: Session):
    return db.query(Alumno).all()

def edit_alumno_by_id(db: Session, user_id: int, name: str, email: str, fecha_ingreso: str = None):
    alumno = get_alumno_by_id(db, user_id)
    if alumno:
        alumno.nombre = name
        alumno.email = email
        if fecha_ingreso:
            alumno.fecha_ingreso = datetime.strptime(fecha_ingreso, '%Y-%m-%d').date()
        db.commit()
        db.refresh(alumno)
        return alumno
    return None

def delete_alumno_by_id(db: Session, user_id: int):
    user = get_alumno_by_id(db, user_id)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

def get_paginated_alumnos(session, page=1, per_page=10):
    return session.query(Alumno).order_by(Alumno.id).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

def enroll_alumno_in_seccion(db: Session, alumno_id: int, seccion_id: int):
    alumno = get_alumno_by_id(db, alumno_id)
    seccion = get_seccion_by_id(db, seccion_id)
    if seccion in alumno.secciones:
        return False, "El alumno ya está inscrito en esta sección."

    alumno.secciones.append(seccion)
    db.commit()
    db.refresh(alumno)
    return True, "Alumno inscrito exitosamente."

def unregister_alumno_in_seccion(db: Session, alumno_id: int, seccion_id: int):
    alumno = get_alumno_by_id(db, alumno_id)
    if not alumno:
        return False, "Alumno no encontrado."

    seccion = get_seccion_by_id(db, seccion_id)
    if not seccion:
        return False, "Sección no encontrada."

    if seccion not in alumno.secciones:
        return False, "El alumno no está inscrito en esta sección."

    alumno.secciones.remove(seccion)
    db.commit()
    return True, "Alumno removido de la sección."

def create_alumno_seccion_from_json(db, data):
    json_is_valid, message = validate_json(data, 'alumnos_seccion')
    if not json_is_valid:
        return False, message
    alumnos_seccion = data.get("alumnos_seccion", [])

    for alumno_seccion in alumnos_seccion:
        alumno_id = alumno_seccion["alumno_id"]
        seccion_id = alumno_seccion["seccion_id"]
        curso_id_of_seccion = get_seccion_by_id(db, seccion_id).curso_id
        check_curso_cerrado(db, curso_id=curso_id_of_seccion)
        enroll_alumno_in_seccion(db, alumno_id, seccion_id)
    return True, f"{len(alumnos_seccion)} alumnos inscritos correctamente"

def create_alumnos_from_json(db: Session, data: dict):
    json_is_valid, message = validate_json(data, 'alumnos')
    if not json_is_valid:
        return False, message
    alumnos_json = data.get("alumnos", [])

    for alumno in alumnos_json:
        create_alumno(
            db=db,
            alumno_id=alumno["id"],
            name=alumno.get("nombre"),
            email=alumno.get("correo"),
            fecha_ingreso=f"{alumno.get('anio_ingreso')}-01-01"
        )
    return True, f"{len(alumnos_json)} alumnos cargados correctamente"
