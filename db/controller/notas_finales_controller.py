from http import HTTPStatus
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from flask import abort
from db.controller.common_controller import get_alumno_by_id
from db.models.notas_finales import NotasFinales
from db.controller.notas_controller import get_notas_by_alumno
from db.utils.math_methods import calculate_average_from_notas

def create_nota_final(db: Session, alumno_id: int, nota_final: float, curso_id: int = None):
    alumno = get_alumno_by_id(db, alumno_id)
    if not alumno:
        abort(HTTPStatus.NOT_FOUND, description=f"Alumno con id {alumno_id} no encontrado.")

    if not isinstance(nota_final, (int, float)):
        abort(HTTPStatus.BAD_REQUEST, description="La nota final debe ser un número.")

    nueva_nota = NotasFinales(
        alumno_id=alumno_id,
        curso_id=curso_id,
        nota_final=nota_final
    )

    try:
        db.add(nueva_nota)
        db.commit()
        db.refresh(nueva_nota)
        print(f"Nota final creada: {nueva_nota.nota_final} para el alumno: {alumno.nombre}")
        return nueva_nota
    except SQLAlchemyError as e:
        db.rollback()
        abort(HTTPStatus.BAD_REQUEST, description=f"Error al guardar la nota final: {str(e)}")

def update_nota_final(db: Session, alumno_id: int, curso_id: int):
    nota_final = calculate_average_nota_alumno(db, alumno_id, curso_id)
    nota_final_obj = get_nota_final(db, alumno_id, curso_id)
    if nota_final_obj:
        nota_final_obj.nota_final = nota_final
    else:
        nota_final_obj = NotasFinales(
            alumno_id=alumno_id,
            curso_id=curso_id,
            nota_final=nota_final
        )
        db.add(nota_final_obj)
    db.commit()

def get_nota_final(db: Session, alumno_id: int, curso_id: int):
    return db.query(NotasFinales).filter(
        NotasFinales.alumno_id == alumno_id,
        NotasFinales.curso_id == curso_id
    ).first()

def get_notas_finales_by_alumno(db: Session, alumno_id: int):
    return db.query(NotasFinales).filter(
        NotasFinales.alumno_id == alumno_id
    ).all()

def get_notas_finales_by_curso(db: Session, curso_id: int):
    return db.query(NotasFinales).filter(
        NotasFinales.curso_id == curso_id
    ).all()

def calculate_average_nota_alumno(db: Session, alumno_id: int, curso_id: int):
    notas = get_notas_by_alumno(db, alumno_id)
    return calculate_average_from_notas(notas, curso_id)
