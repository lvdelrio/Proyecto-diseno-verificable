from sqlalchemy.orm import Session
from ..models.curso import Curso
from ..models.seccion import Seccion

def create_seccion(db: Session, curso_id: int, nombre: str):
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        return None
    
    new_seccion = Seccion(nombre=nombre, curso=curso)
    db.add(new_seccion)
    db.commit()
    db.refresh(new_seccion)
    return new_seccion

def get_seccion_by_id(db: Session, new_seccion: int):
    return db.query(Seccion).filter(Seccion.id == new_seccion).first()

def get_all_secciones_by_curso_id(db: Session, curso_id: int):
    return db.query(Seccion).filter(Seccion.curso_id ==curso_id).all()

def get_all_secciones(db: Session):
    return db.query(Seccion).all()


def edit_seccion_by_id(db: Session, seccion_id: int, nombre: str):
    seccion = db.query(Seccion).filter(Seccion.id == seccion_id).first()
    if seccion:
        seccion.nombre = nombre
        db.commit()
        db.refresh(seccion)
        return seccion
    return None

def delete_seccion_by_id(db: Session, seccion_id: int):
    seccion = db.query(Seccion).filter(Seccion.id == seccion_id).first()
    if seccion:
        db.delete(seccion)
        db.commit()
        return True
    return False

def curso_from_seccion_id(db: Session, seccion_id: int):
    seccion = db.query(Seccion).filter(Seccion.id == seccion_id).first()
    if seccion:
        return seccion.curso_id
    return False