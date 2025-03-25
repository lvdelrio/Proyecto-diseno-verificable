from sqlalchemy.orm import Session
from ..models.alumno import Alumno

def crear_alumno(db: Session, name: str, email: str):
    new_user = Alumno(nombre=name, email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_alumno_by_id(db: Session, user_id: int):
    return db.query(Alumno).filter(Alumno.id == user_id).first()

def get_all_alumnos(db: Session):
    return db.query(Alumno).all()

