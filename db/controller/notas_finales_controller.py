from sqlalchemy.orm import Session
from flask import abort
from db.models.alumno import Alumno
from db.controller.alumno_controller import get_alumno_by_id
from db.models.notas_finales import NotasFinales
from .notas_controller import calculate_promedio_alumno

def create_nota_final(db: Session, alumno_id: int, nota_final: float, curso_id: int = None):
    alumno = get_alumno_by_id(db, alumno_id)
    if not alumno:
        abort(404, description=f"Alumno con id {alumno_id} no encontrado.")

    if not isinstance(nota_final, (int, float)):
        abort(400, description="La nota final debe ser un número.")

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
    except Exception as e:
        db.rollback()
        abort(400, description=f"Error al guardar la nota final: {str(e)}")


def update_nota_final(db: Session, alumno_id: int, curso_id: int, nota_final: float):
    nota_existente = db.query(NotasFinales).filter(
        NotasFinales.alumno_id == alumno_id,
        NotasFinales.curso_id == curso_id
    ).first()
    
    if nota_existente:
        nota_existente.nota_final = nota_final
        db.commit()
    return nota_existente

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

def calculate_nota_final(db: Session, alumno_id: int, curso_id: int):
    promedio = calculate_promedio_alumno(db, alumno_id)
    if promedio is not None:
        return create_nota_final(db, alumno_id, curso_id, promedio)
    return None