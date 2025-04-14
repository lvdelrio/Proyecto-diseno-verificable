from db.config import db
from db.models.evaluacion import Evaluacion
from db.models.notas import Notas
from db.models.alumno import Alumno
from db.models.categoria_evaluacion import CategoriaEvaluacion
from db.models.alumno_seccion import AlumnoSeccion

def crear_evaluacion_con_notas(tipo, id_categoria, ponderacion, opcional):
    evaluacion = Evaluacion(
        tipo=tipo,
        id_categoria=id_categoria,
        ponderacion=ponderacion,
        opcional=opcional
    )
    db.session.add(evaluacion)
    db.session.commit()

    alumnos_seccion = get_all_alumnos_seccion()

    notas_vacias = [
        Notas(alumno_id=alumno_sec.id_alumno, evaluacion_id=evaluacion.id, nota=None)
        for alumno_sec in alumnos_seccion
    ]

    db.session.add_all(notas_vacias)
    db.session.commit()

    return evaluacion

def crear_evaluacion(tipo, ponderacion, opcional, categoria):
    nueva_evaluacion = Evaluacion(
        tipo=tipo,
        ponderacion=ponderacion,
        opcional=opcional,
        categoria=categoria
    )
    db.session.add(nueva_evaluacion)
    db.session.commit()
    return nueva_evaluacion

def obtener_evaluacion(evaluacion_id):
    return Evaluacion.query.get(evaluacion_id)

def actualizar_evaluacion(evaluacion_id, **kwargs):
    evaluacion = Evaluacion.query.get(evaluacion_id)
    for key, value in kwargs.items():
        setattr(evaluacion, key, value)
    db.session.commit()
    return evaluacion

def eliminar_evaluacion(evaluacion_id):
    evaluacion = Evaluacion.query.get(evaluacion_id)
    db.session.delete(evaluacion)
    db.session.commit()

