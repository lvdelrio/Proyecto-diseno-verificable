from sqlalchemy.orm import Session
from ..models.curso import Curso

def create_curso(db: Session, name: str, description: str, imparted_semester: str):
    new_curso= Curso(nombre=name, descripcion=description, semestre_impartido=imparted_semester)
    db.add(new_curso)
    db.commit()
    db.refresh(new_curso)
    return new_curso

def get_curso_by_id(db: Session, curso_id: int):
    return db.query(Curso).filter(Curso.id == curso_id).first()

def get_all_cursos(db: Session):
    return db.query(Curso).all()


def edit_curso_by_id(db: Session, course_id: int, name: str, description: str, imparted_semester: str):
    curso = db.query(Curso).filter(Curso.id == course_id).first()
    if curso:
        curso.nombre = name
        curso.descripcion = description
        curso.semestre_impartido = imparted_semester
        db.commit()
        db.refresh(curso)
        return curso
    return None

def delete_curso_by_id(db: Session, curso_id: int):
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if curso:
        db.delete(curso)
        db.commit()
        return True
    return False