from sqlalchemy.orm import Session
from db.models.seccion import Seccion
from db.controller.profesor_controller import enroll_profesor_in_seccion
from db.controller.categoria_controller import create_multiple_categorias_and_evaluaciones
from db.controller.curso_controller import get_curso_by_id
from db.controller.common_controller import get_seccion_by_id
from db.services.curso_service import check_curso_cerrado

def create_seccion(db: Session, curso_id: int, nombre: str, seccion_id: int = None):
    curso = get_curso_by_id(db, curso_id)
    if not curso_id:
        return None
    if seccion_id is not None:
        new_seccion = Seccion(id=seccion_id, nombre=nombre, curso_id=curso_id)
    else:
        new_seccion = Seccion(nombre=nombre, curso=curso)
    try:
        db.add(new_seccion)
        db.commit()
        db.refresh(new_seccion)
        return new_seccion
    except Exception as e:
        db.rollback()
        print(f"Error creating seccion: {e}")
        return None

def get_all_secciones_by_curso_id(db: Session, curso_id: int):
    return db.query(Seccion).filter(Seccion.curso_id ==curso_id).all()

def get_all_secciones(db: Session):
    return db.query(Seccion).all()


def edit_seccion_by_id(db: Session, seccion_id: int, nombre: str):
    seccion = get_seccion_by_id(db, seccion_id)
    if seccion:
        seccion.nombre = nombre
        db.commit()
        db.refresh(seccion)
        return seccion
    return None

def delete_seccion_by_id(db: Session, seccion_id: int):
    seccion = get_seccion_by_id(db, seccion_id)
    if seccion:
        db.delete(seccion)
        db.commit()
        return True
    return False

def curso_from_seccion_id(db: Session, seccion_id: int):
    seccion = get_seccion_by_id(db, seccion_id)
    if seccion:
        return seccion.curso_id
    return False

def create_secciones_from_json(db: Session, data: dict):
    secciones_json = data.get("secciones", [])
    for seccion_data in secciones_json:
        process_seccion_and_relations(db, seccion_data)
    db.commit()

def process_seccion_and_relations( db: Session, seccion_data: dict):
    curso_id = seccion_data.get("instancia_curso")
    check_curso_cerrado(db, curso_id=curso_id)
    seccion = create_seccion(
        db,
        seccion_id=seccion_data["id"],
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
