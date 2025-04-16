from sqlalchemy.orm import Session
from ..models.curso import Curso

def create_curso(db: Session, tipo_curso_id: int, fecha_impartida: int, semestre_impartido: str):
    new_curso = Curso(tipo_curso_id=tipo_curso_id, fecha_impartida=fecha_impartida, semestre_impartido=semestre_impartido)
    db.add(new_curso)
    db.commit()
    db.refresh(new_curso)
    return new_curso

def get_curso_by_id(db: Session, curso_id: int):
    return db.query(Curso).filter(Curso.id == curso_id).first()

def get_all_cursos(db: Session):
    return db.query(Curso).all()


def edit_curso_by_id(db: Session, curso_id: int, tipo_curso_id: int, fecha_impartida: int, semestre_impartido: str):
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if curso:
        curso.tipo_curso_id=tipo_curso_id
        curso.fecha_impartida=fecha_impartida
        curso.semestre_impartido = semestre_impartido
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