from sqlalchemy.orm import Session
from ..models.profesor import Profesor
from ..models.seccion import Seccion
from ..controller.common_controller import get_seccion_by_id, get_profesor_by_id

def create_profesor(db: Session, nombre: str, email: str, id: int = None):
    if id is not None:
        new_profesor = Profesor(id=id, nombre=nombre, email=email)
    else:
        new_profesor= Profesor(nombre=nombre, email=email)
    db.add(new_profesor)
    db.commit()
    db.refresh(new_profesor)
    return new_profesor

def get_all_profesores(db: Session):
    return db.query(Profesor).all()


def edit_profesor_by_id(db: Session, profesor_id: int, nombre: str, email: str):
    profesor = get_profesor_by_id(db, profesor_id)
    if profesor:
        profesor.nombre = nombre
        profesor.email = email
        db.commit()
        db.refresh(profesor)
        return profesor
    return None

def delete_profesor_by_id(db: Session, professor_id: int):
    profesor = get_profesor_by_id(db, professor_id)
    if profesor:
        db.delete(profesor)
        db.commit()
        return True
    return False

def get_paginated_profesores(session, page=1, per_page=10):
    return session.query(Profesor).order_by(Profesor.id).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

def enroll_profesor_in_seccion(db: Session, profesor_id: int, seccion_id: int):
    profesor = get_profesor_by_id(db, profesor_id)
    if not profesor:
        return False, "Profesor no encontrado."

    seccion = get_seccion_by_id(db, seccion_id)
    if not seccion:
        return False, "Sección no encontrada."

    if seccion in profesor.secciones:
        return False, "El profesor ya está inscrito en esta sección."

    profesor.secciones.append(seccion)
    db.commit()
    db.refresh(profesor)

    return True, "Profesor inscrito exitosamente."

def unregister_profesor_in_seccion(db: Session, seccion_id: int, profesor_id: int):
    profesor = get_profesor_by_id(db, profesor_id)
    if not profesor:
        return False, "Profesor no encontrado."

    seccion = get_seccion_by_id(db, seccion_id)
    if not seccion:
        return False, "Sección no encontrada."

    if seccion not in profesor.secciones:
        return False, "El profesor no está inscrito en esta sección."

    profesor.secciones.remove(seccion)
    db.commit()
    return True, "Profesor removido de la sección."

def create_profesores_from_json(db: Session, data: dict):
    profesores_json = data.get("profesores", [])

    for profesor in profesores_json:
        create_profesor(
            db=db,
            id=profesor["id"],
            nombre=profesor.get("nombre"),
            email=profesor.get("correo")
        )