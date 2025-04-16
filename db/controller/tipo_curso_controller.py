from sqlalchemy.orm import Session
from ..models.tipo_curso import TipoCurso
from ..models.requisitos import CursoRequisito

def create_tipo_curso(db: Session, name: str, description: str):
    new_tipo_curso= TipoCurso(nombre=name, descripcion=description)
    db.add(new_tipo_curso)
    db.commit()
    db.refresh(new_tipo_curso)
    return new_tipo_curso

def get_tipo_curso_by_id(db: Session, tipo_curso_id: int):
    return db.query(TipoCurso).filter(TipoCurso.id == tipo_curso_id).first()

def get_all_tipo_cursos(db: Session):
    return db.query(TipoCurso).all()


def edit_tipo_curso_by_id(db: Session, tipo_curso_id: int, name: str, description: str):
    tipo_curso = db.query(TipoCurso).filter(TipoCurso.id == tipo_curso_id).first()
    if tipo_curso:
        tipo_curso.nombre = name
        tipo_curso.descripcion = description
        db.commit()
        db.refresh(tipo_curso)
        return tipo_curso
    return None

def delete_tipo_curso_by_id(db: Session, tipo_curso_id: int):
    tipo_curso = db.query(TipoCurso).filter(TipoCurso.id == tipo_curso_id).first()
    print(tipo_curso)
    if tipo_curso:
        db.delete(tipo_curso)
        db.commit()
        return True
    return False

def add_requisito_tipo_curso(db: Session, tipo_curso_id: int):
    tipo_curso = db.query(TipoCurso).filter(TipoCurso.id == tipo_curso_id).first()
    if tipo_curso:
        db.delete(tipo_curso)
        db.commit()
        return True
    return False


def enroll_tipo_curso_in_tipo_cursos(db: Session, tipo_curso_base_id: int, tipo_curso_id: int):
    if tipo_curso_base_id == tipo_curso_id:
        return False, "Un tipo de curso no puede ser requisito de sí mismo."

    existing = db.query(CursoRequisito).filter_by(
        tipo_curso_id=tipo_curso_base_id,
        curso_requisito_id=tipo_curso_id
    ).first()

    if existing:
        return False, "Este requisito ya está asignado."

    nuevo_requisito = CursoRequisito(
        tipo_curso_id=tipo_curso_base_id,
        curso_requisito_id=tipo_curso_id
    )
    db.add(nuevo_requisito)
    db.commit()
    return True, "Requisito agregado exitosamente."
