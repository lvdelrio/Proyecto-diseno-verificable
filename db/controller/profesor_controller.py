from sqlalchemy.orm import Session
from ..models.profesor import Profesor

def crear_profesor(db: Session, nombre: str, email: str):
    new_profesor= Profesor(nombre=nombre, email=email)
    db.add(new_profesor)
    db.commit()
    db.refresh(new_profesor)
    return new_profesor

def get_profesor_by_id(db: Session, new_profesor: int):
    return db.query(Profesor).filter(Profesor.id == new_profesor).first()

def get_all_profesores(db: Session):
    return db.query(Profesor).all()


def edit_profesor_by_id(db: Session, profesor_id: int, nombre: str, email: str):
    profesor = db.query(Profesor).filter(Profesor.id == profesor_id).first()
    if profesor:
        profesor.nombre = nombre
        profesor.email = email
        db.commit()
        db.refresh(profesor)
        return profesor
    return None

def delete_profesor_by_id(db: Session, new_profesor: int):
    profesor = db.query(Profesor).filter(Profesor.id == new_profesor).first()
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