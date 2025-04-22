from flask import abort
from sqlalchemy.orm import Session
from ..models.curso import Curso
from ..models.seccion import Seccion
from ..models.profesor import Profesor
from ..models.evaluacion import Evaluacion
from ..models.categoria import Categoria
from ..controller.profesor_controller import enroll_profesor_in_seccion
from ..controller.categoria_controller import create_multiple_categorias_and_evaluaciones
from ..controller.evaluacion_controller import create_evaluacion

def create_seccion(db: Session, curso_id: int, nombre: str, id: int = None):
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        return None
    if id is not None:
        new_seccion = Seccion(id=id, nombre=nombre, curso=curso)
    else:
        new_seccion = Seccion(nombre=nombre, curso=curso)
    db.add(new_seccion)
    db.commit()
    db.refresh(new_seccion)
    return new_seccion

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

def create_secciones_from_json(db: Session, data: dict):
    secciones_json = data.get("secciones", [])    
    for seccion_data in secciones_json:
        process_seccion_and_relations(db, seccion_data)
    db.commit()

def process_seccion_and_relations( db: Session, seccion_data: dict):
    seccion = create_seccion(
        db,
        id=seccion_data["id"],
        nombre=f"Seccion {seccion_data['id']}",
        curso_id=seccion_data["instancia_curso"]
    )

    if "profesor_id" in seccion_data:
        enroll_profesor_in_seccion(
            db,
            profesor_id=seccion_data["profesor_id"],
            seccion_id=seccion.id
        )
    create_multiple_categorias_and_evaluaciones(db, seccion, seccion_data.get("evaluacion", {}))



