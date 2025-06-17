from http import HTTPStatus
from flask import abort
from sqlalchemy.orm import Session
from db.models.curso import Curso
from db.utils.json_validator import validate_json

def create_curso(db: Session, tipo_curso_id: int, fecha_impartida: int,
                  semestre_impartido: str, curso_id: int = None):
    if curso_id is not None:
        new_curso = Curso(id=curso_id,
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

def edit_curso_by_id(db: Session, curso_id: int, tipo_curso_id: int,
                      fecha_impartida: int, semestre_impartido: str):
    curso = get_curso_by_id(db, curso_id)
    if curso:
        if curso.cerrado:
            abort(HTTPStatus.FORBIDDEN,
                  description="El curso está cerrado y ya no se puede modificar")
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

def close_curso(db: Session, curso_id: int):
    curso = get_curso_by_id(db, curso_id)
    if curso:
        curso.cerrado = True
        db.commit()
        db.refresh(curso)
        return curso
    return None

def open_curso(db: Session, curso_id: int):
    curso = get_curso_by_id(db, curso_id)
    if curso:
        curso.cerrado = False
        db.commit()
        db.refresh(curso)
        return curso
    return None

def create_cursos_from_json(db: Session, data: dict):
    json_is_valid, message = validate_json(data, "cursos")
    if not json_is_valid:
        return False, message
    instancias_json = data.get("instancias", [])
    for instancia in instancias_json:
        create_curso(
            db=db,
            curso_id=instancia["id"],
            tipo_curso_id=instancia.get("curso_id"),
            fecha_impartida=data.get("año"),
            semestre_impartido=data.get("semestre")
        )
    return True, f"{len(instancias_json)} instancias de curso cargadas correctamente."
