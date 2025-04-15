from db.config import db
from db.models.evaluacion import Evaluacion
from db.models.notas import Notas
from db.models.alumno import Alumno
from db.models.categoria import Categoria
from db.models.alumno_seccion import AlumnoSeccion
from flask import abort

def create_evaluacion_con_notas(tipo, id_categoria, ponderacion, opcional):
    evaluacion = Evaluacion(
        tipo=tipo,
        id_categoria=id_categoria,
        ponderacion=ponderacion,
        opcional=opcional
    )
    db.session.add(evaluacion)
    db.session.commit()

    #esta funcion  no existe
    alumnos_seccion = get_all_alumnos_seccion()

    notas_vacias = [
        Notas(alumno_id=alumno_sec.id_alumno, evaluacion_id=evaluacion.id, nota=None)
        for alumno_sec in alumnos_seccion
    ]

    db.session.add_all(notas_vacias)
    db.session.commit()

    return evaluacion

def create_evaluacion(tipo, ponderacion, opcional, categoria = None):
    nueva_evaluacion = Evaluacion(
        tipo=tipo,
        ponderacion=ponderacion,
        opcional=opcional,
        categoria=categoria
    )
    db.session.add(nueva_evaluacion)
    db.session.commit()
    return nueva_evaluacion

def get_evaluacion(evaluacion_id):
    return Evaluacion.query.get(evaluacion_id)

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

def delete_evaluacion(evaluacion_id):
    evaluacion = Evaluacion.query.get(evaluacion_id)
    db.session.delete(evaluacion)
    db.session.commit()

