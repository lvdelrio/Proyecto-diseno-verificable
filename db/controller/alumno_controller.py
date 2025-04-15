from datetime import datetime
from sqlalchemy.orm import Session
from ..models.alumno import Alumno
from ..models.seccion import Seccion

def create_alumno(db: Session, name: str, email: str, fecha_ingreso: str = None):
    fecha_ingreso_dt = datetime.strptime(fecha_ingreso, '%Y-%m-%d').date() if fecha_ingreso else None
    
    new_user = Alumno(
        nombre=name,
        email=email,
        fecha_ingreso=fecha_ingreso_dt
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_alumno_by_id(db: Session, user_id: int):
    return db.query(Alumno).filter(Alumno.id == user_id).first()

def get_all_alumnos(db: Session):
    return db.query(Alumno).all()

def edit_alumno_by_id(db: Session, user_id: int, name: str, email: str, fecha_ingreso: str = None):
    alumno = db.query(Alumno).filter(Alumno.id == user_id).first()
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
    user = db.query(Alumno).filter(Alumno.id == user_id).first()
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
    alumno = db.query(Alumno).filter(Alumno.id == alumno_id).first()
    if not alumno:
        return False, "Alumno no encontrado."

    seccion = db.query(Seccion).filter(Seccion.id == seccion_id).first()
    if not seccion:
        return False, "Sección no encontrada."

    if seccion in alumno.secciones:
        return False, "El alumno ya está inscrito en esta sección."

    alumno.secciones.append(seccion)
    db.commit()
    db.refresh(alumno)

    return True, "Alumno inscrito exitosamente."