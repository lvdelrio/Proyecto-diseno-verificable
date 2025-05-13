from sqlalchemy.orm import Session
from flask import abort
from datetime import datetime
from db.config import db
from db.models.evaluacion import Evaluacion
from db.models.notas import Notas
from db.models.alumno import Alumno
from db.models.categoria import Categoria
from db.models.alumno_seccion import AlumnoSeccion
from ..controller.common_controller import get_all_alumno_seccion_by_categoria_id, get_evaluaciones_by_categoria_id
from ..controller.notas_controller import create_nota
from db.utils.prorrotear import recalculate_categoria_ponderations
from ...utils.http_status import BAD_REQUEST, NOT_FOUND

PERCENTAGE_TYPE = 1
MAX_PERCENTAGE = 100

def create_evaluacion(db: Session, nombre: str, ponderacion: float, opcional: bool, categoria_id: int = None, tipo_ponderacion: bool = False):
    nueva_evaluacion = Evaluacion(
        nombre=nombre,
        ponderacion=ponderacion,
        opcional=opcional,
        categoria_id=categoria_id,
        tipo_ponderacion=tipo_ponderacion
    )

    if not validation_evaluacion(nueva_evaluacion, categoria_id):
        abort(BAD_REQUEST, description="Error: La evaluación no es válida para la categoría.")
        return
    db.add(nueva_evaluacion)
    db.commit()
    db.refresh(nueva_evaluacion)
    if(percentage_sum_from_categoria_by_id(db, nueva_evaluacion.categoria_id) > MAX_PERCENTAGE and
           nueva_evaluacion.tipo_ponderacion == PERCENTAGE_TYPE):
            recalculate_categoria_ponderations(db, nueva_evaluacion.categoria_id)
    return nueva_evaluacion

def create_evaluacion_con_notas(db: Session, nombre: str, ponderacion: float, opcional: bool, categoria_id: int = None, tipo_ponderacion: bool = False):
    
    nueva_evaluacion = create_evaluacion(db, nombre, ponderacion, opcional, categoria_id, tipo_ponderacion)
    alumnos_seccion = get_all_alumno_seccion_by_categoria_id(db, categoria_id)
    if not alumnos_seccion:
        raise ValueError("No hay alumnos en la sección especificada.")

    notas_vacias = [
        create_nota(db=db, alumno_id=alumno.id, evaluacion_id=nueva_evaluacion.id, nota=None)
        for alumno in alumnos_seccion
    ]

    db.add_all(notas_vacias)
    db.commit()

    return nueva_evaluacion

def get_evaluacion_by_id(db: Session, evaluacion_id: int):
    return db.query(Evaluacion).filter(Evaluacion.id == evaluacion_id).first()

def get_all_evaluaciones(db: Session):
    return db.query(Evaluacion).all()

def edit_evaluacion(db: Session, evaluacion_id, nombre=None, ponderacion=None, opcional=None, categoria_id=None, tipo_ponderacion=None):
    evaluacion = get_evaluacion_by_id(db, evaluacion_id)
    if not evaluacion:
        abort(NOT_FOUND, description="Evaluación no encontrada")

    if nombre is not None:
        evaluacion.nombre = nombre
    if ponderacion is not None:
        evaluacion.ponderacion = ponderacion
    if opcional is not None:
        evaluacion.opcional = opcional
    if categoria_id is not None:
        evaluacion.categoria_id = categoria_id
    if tipo_ponderacion is not None and tipo_ponderacion != evaluacion.tipo_ponderacion:
        evaluacion.tipo_ponderacion = tipo_ponderacion
        update_tipo_ponderacion_in_categoria(db, evaluacion.categoria_id, tipo_ponderacion)

    try:
        db.commit()
        if(percentage_sum_from_categoria_by_id(db, evaluacion.categoria_id) > MAX_PERCENTAGE and
           evaluacion.tipo_ponderacion == PERCENTAGE_TYPE):
            recalculate_categoria_ponderations(db, evaluacion.categoria_id)
        return evaluacion
    except Exception as e:
        db.rollback()
        abort(BAD_REQUEST, description=f"Error al actualizar la evaluación: {str(e)}")

def percentage_sum_from_categoria_by_id(db: Session, categoria_id: int):
    evaluaciones = get_evaluaciones_by_categoria_id(db, categoria_id)
    percentage_sum = sum(evaluacion.ponderacion for evaluacion in evaluaciones)
    return percentage_sum

def delete_evaluacion(db: Session, evaluacion_id: int):
    evaluacion = get_evaluacion_by_id(db, evaluacion_id)
    if evaluacion:
        db.delete(evaluacion)
        db.commit()
        return True
    return False

def get_last_evaluacion_by_category(category_id):
    last_evaluacion = Evaluacion.query.filter_by(categoria_id=category_id).order_by(Evaluacion.id.desc()).first()
    return last_evaluacion

def validation_evaluacion(nueva_evaluacion, categoria_id):
    last_evaluacion = get_last_evaluacion_by_category(categoria_id)
    if last_evaluacion is None:
        return True
    return last_evaluacion.tipo_ponderacion == nueva_evaluacion.tipo_ponderacion

def update_tipo_ponderacion_in_categoria(db: Session, categoria_id: int, nuevo_tipo: bool):
    evaluaciones = get_evaluaciones_by_categoria_id(db, categoria_id)
    for evaluacion in evaluaciones:
        evaluacion.tipo_ponderacion = nuevo_tipo
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        abort(BAD_REQUEST, description=f"Error al actualizar tipo de ponderación en evaluaciones: {str(e)}")
