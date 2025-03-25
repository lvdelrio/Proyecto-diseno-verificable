from sqlalchemy.orm import Session
from ..models.curso import Curso

def crear_curso(db: Session, name: str, description: str):
    new_course= Curso(nombre=name, descripcion=description)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

def get_curso_by_id(db: Session, course_id: int):
    return db.query(Curso).filter(Curso.id == course_id).first()

def get_all_cursos(db: Session):
    return db.query(Curso).all()


def edit_curso_by_id(db: Session, course_id: int, name: str, description: str):
    curso = db.query(Curso).filter(Curso.id == course_id).first()
    if curso:
        curso.nombre = name
        curso.descripcion = description
        db.commit()
        db.refresh(curso)
        return curso
    return None

def delete_curso_by_id(db: Session, course_id: int):
    curso = db.query(Curso).filter(Curso.id == course_id).first()
    if curso:
        db.delete(curso)
        db.commit()
        return True
    return False