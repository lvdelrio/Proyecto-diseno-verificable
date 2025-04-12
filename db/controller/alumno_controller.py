from datetime import datetime
from sqlalchemy.orm import Session
from ..models.alumno import Alumno

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
    user = db.query(Alumno).filter(Alumno.id == user_id).first()
    if user:
        user.nombre = name
        user.email = email
        if fecha_ingreso:
            user.fecha_ingreso = datetime.strptime(fecha_ingreso, '%Y-%m-%d').date()
        db.commit()
        db.refresh(user)
        return user
    return None

def delete_alumno_by_id(db: Session, user_id: int):
    user = db.query(Alumno).filter(Alumno.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

def get_paginated_alumnos(session, pagina=1, por_pagina=10):
    return session.query(Alumno).order_by(Alumno.id).paginate(
        page=pagina,
        per_page=por_pagina,
        error_out=False
    )