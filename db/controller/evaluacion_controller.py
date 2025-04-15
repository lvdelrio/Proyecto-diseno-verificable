from sqlalchemy.orm import Session
from flask import abort
from datetime import datetime
from db.config import db
from db.models.evaluacion import Evaluacion
from db.models.notas import Notas
from db.models.alumno import Alumno
from db.models.categoria import Categoria
from db.models.alumno_seccion import AlumnoSeccion

def create_evaluacion(db: Session, tipo: int, ponderacion: float, opcional: bool, categoria_id: int = None):
    nueva_evaluacion = Evaluacion(
        tipo=tipo,
        ponderacion=ponderacion,
        opcional=int(opcional),
        categoria_id=categoria_id
    )
    db.add(nueva_evaluacion)
    db.commit()
    db.refresh(nueva_evaluacion)
    return nueva_evaluacion

def create_evaluacion_con_notas(db: Session, tipo: int, ponderacion: float, opcional: bool, categoria_id: int = None):
    nueva_evaluacion = Evaluacion(
        tipo=tipo,
        ponderacion=ponderacion,
        opcional=int(opcional),
        categoria_id=categoria_id
    )
    db.add(nueva_evaluacion)
    db.commit()
    db.refresh(nueva_evaluacion)

    alumnos_seccion = db.query(AlumnoSeccion).filter(AlumnoSeccion.categoria_id == categoria_id).all()
    if not alumnos_seccion:
        raise ValueError("No hay alumnos en la sección especificada.")

    notas_vacias = [
        Notas(alumno_id=alumno.id, evaluacion_id=nueva_evaluacion.id, nota=None)
        for alumno in alumnos_seccion
    ]

    db.add_all(notas_vacias)
    db.commit()

    return nueva_evaluacion

def get_evaluacion_by_id(db: Session, evaluacion_id: int):
    return db.query(Evaluacion).filter(Evaluacion.id == evaluacion_id).first()

def get_all_evaluaciones(db: Session):
    return db.query(Evaluacion).all()

def get_evaluaciones_by_seccion(db: Session, categoria_id: int):
    return db.query(Evaluacion).filter(Evaluacion.categoria_id == categoria_id).all()

def edit_evaluacion(evaluacion_id, tipo=None, ponderacion=None, opcional=None, categoria_id=None):

    evaluacion = Evaluacion.query.get(evaluacion_id)
    if not evaluacion:
        abort(404, description="Evaluación no encontrada")

    if tipo is not None:
        evaluacion.tipo = tipo
    if ponderacion is not None:
        evaluacion.ponderacion = ponderacion
    if opcional is not None:
        evaluacion.opcional = opcional
    if categoria_id is not None:
        evaluacion.categoria_id = categoria_id
    
    try:
        db.session.commit()
        return evaluacion
    except Exception as e:
        db.session.rollback()
        abort(400, description=f"Error al actualizar la evaluación: {str(e)}")

def delete_evaluacion(db: Session, evaluacion_id: int):
    evaluacion = db.query(Evaluacion).filter(Evaluacion.id == evaluacion_id).first()
    if evaluacion:
        db.delete(evaluacion)
        db.commit()
        return True
    return False