from sqlalchemy.orm import Session
from flask import abort
from datetime import datetime
from db.config import db
from db.models.evaluacion import Evaluacion
from db.models.notas import Notas
from db.models.alumno import Alumno
from db.models.categoria import Categoria
from db.models.alumno_seccion import AlumnoSeccion
from ..controller.common_controller import get_all_alumno_seccion_by_categoria_id
from ..controller.notas_controller import create_nota

def create_evaluacion(db: Session, nombre: str, ponderacion: float, opcional: bool, categoria_id: int = None, tipo_ponderacion: bool = False):
    nueva_evaluacion = Evaluacion(
        nombre=nombre,
        ponderacion=ponderacion,
        opcional=opcional,
        categoria_id=categoria_id,
        tipo_ponderacion=tipo_ponderacion
    )

    if not validation_evaluacion(nueva_evaluacion, categoria_id):
        abort(400, description="Error: La evaluación no es válida para la categoría.")
        return
    db.add(nueva_evaluacion)
    db.commit()
    db.refresh(nueva_evaluacion)
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

def get_evaluaciones_by_seccion(db: Session, categoria_id: int):
    return db.query(Evaluacion).filter(Evaluacion.categoria_id == categoria_id).all()

def get_evaluaciones_by_categoria(db: Session, categoria_id: int):
    return db.query(Evaluacion).filter(Evaluacion.categoria_id == categoria_id).all()

def edit_evaluacion(evaluacion_id, nombre=None, ponderacion=None, opcional=None, categoria_id=None, tipo_ponderacion=None):
    evaluacion = get_evaluacion_by_id(db, evaluacion_id)
    if not evaluacion:
        abort(404, description="Evaluación no encontrada")

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
        actualizar_tipo_ponderacion_en_categoria(evaluacion.categoria_id, tipo_ponderacion)

    try:
        db.session.commit()
        return evaluacion
    except Exception as e:
        db.session.rollback()
        abort(400, description=f"Error al actualizar la evaluación: {str(e)}")

def delete_evaluacion(db: Session, evaluacion_id: int):
    evaluacion = get_evaluacion_by_id(db, evaluacion_id)
    if evaluacion:
        db.delete(evaluacion)
        db.commit()
        return True
    return False

def get_last_evaluation_by_category(category_id):
    last_evaluation = Evaluacion.query.filter_by(categoria_id=category_id).order_by(Evaluacion.id.desc()).first()
    return last_evaluation

def validation_evaluacion(nueva_evaluacion, categoria_id):
    last_evaluation = get_last_evaluation_by_category(categoria_id)
    if last_evaluation is None:
        return True
    return last_evaluation.tipo_ponderacion == nueva_evaluacion.tipo_ponderacion

def actualizar_tipo_ponderacion_en_categoria(categoria_id: int, nuevo_tipo: bool):
    evaluaciones = get_evaluaciones_by_categoria(db, categoria_id)
    for evaluacion in evaluaciones:
        evaluacion.tipo_ponderacion = nuevo_tipo
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(400, description=f"Error al actualizar tipo de ponderación en evaluaciones: {str(e)}")
