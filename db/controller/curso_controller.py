from sqlalchemy.orm import Session
from ..models.curso import Curso

def create_curso(db: Session, tipo_curso_id: int, fecha_impartida: int, semestre_impartido: str, id: int = None):
    if id is not None:
        new_curso = Curso(id=id, 
                        tipo_curso_id=tipo_curso_id, 
                        fecha_impartida=fecha_impartida, 
                        semestre_impartido=semestre_impartido)
    else:
        new_curso = Curso(tipo_curso_id=tipo_curso_id, 
                          fecha_impartida=fecha_impartida, 
                          semestre_impartido=semestre_impartido)
    db.add(new_curso)
    db.commit()
    db.refresh(new_curso)
    return new_curso

def get_curso_by_id(db: Session, curso_id: int):
    return db.query(Curso).filter(Curso.id == curso_id).first()

def get_all_cursos(db: Session):
    return db.query(Curso).all()


def edit_curso_by_id(db: Session, curso_id: int, tipo_curso_id: int, fecha_impartida: int, semestre_impartido: str):
    curso = get_curso_by_id(db, curso_id)
    if curso:
        curso.tipo_curso_id=tipo_curso_id
        curso.fecha_impartida=fecha_impartida
        curso.semestre_impartido = semestre_impartido
        db.commit()
        db.refresh(curso)
        return curso
    return None

def delete_curso_by_id(db: Session, curso_id: int):
    curso = get_curso_by_id(db, curso_id)
    if curso:
        db.delete(curso)
        db.commit()
        return True
    return False

def create_cursos_from_json(db: Session, data: dict):
    if not data or "instancias" not in data:
        raise ValueError("No se recibió JSON válido o no contiene 'instancias'.")
    instancias_json = data.get("instancias", [])
    for instancia in instancias_json:
        create_curso(
            db=db,
            id=instancia["id"],
            tipo_curso_id=instancia.get("curso_id"),
            fecha_impartida=data.get("año"),
            semestre_impartido=data.get("semestre")
        )