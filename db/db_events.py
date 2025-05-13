from flask import abort
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from .models.curso import Curso
from .models.seccion import Seccion
from .models.categoria import Categoria
from .models.evaluacion import Evaluacion
from .models.notas import Notas
from .models.alumno_seccion import AlumnoSeccion
from .models.profesor_seccion import ProfesorSeccion
from .config import db 
from .controller.common_controller import get_seccion_by_id 
from .controller.categoria_controller import get_categoria
from .controller.evaluacion_controller import get_evaluacion_by_id
session = db.session

def verificar_curso_abierto(mapper, connection, target):

    curso_id = obtener_curso_id(target)
    if curso_id:
        curso = session.query(Curso).filter_by(id=curso_id).first()
        if curso and curso.cerrado:
            abort(403, description=f"El curso id {curso_id} está cerrado y ya no se puede modificar")

def obtener_curso_id(target):
    if isinstance(target, Seccion):
        return target.curso_id
    if isinstance(target, Categoria):
        return obtener_curso_id_from_categoria(target)
    if isinstance(target, Evaluacion):
        return obtener_curso_id_from_evaluacion(target)
    if isinstance(target, Notas):
        return obtener_curso_id_from_notas(target)
    if isinstance(target, AlumnoSeccion):
        return obtener_curso_id_from_seccion(target, 'seccion_id')
    if isinstance(target, ProfesorSeccion):
        return obtener_curso_id_from_seccion(target, 'seccion_id')
    return None

def obtener_curso_id_from_categoria(target):
    if hasattr(target, 'seccion') and target.seccion:
        return target.seccion.curso_id
    if hasattr(target, 'id_seccion'):
        seccion = session.query(Seccion).filter_by(id=target.id_seccion).first()
        return seccion.curso_id if seccion else None
    return None

def obtener_curso_id_from_evaluacion(target):
    if hasattr(target, 'categoria') and target.categoria:
        return obtener_curso_id_from_categoria(target.categoria)
    if hasattr(target, 'categoria_id'):
        categoria = get_categoria(target.categoria_id)
        return obtener_curso_id_from_categoria(categoria) if categoria else None
    return None

def obtener_curso_id_from_notas(target):
    if hasattr(target, 'evaluacion') and target.evaluacion:
        return obtener_curso_id_from_evaluacion(target.evaluacion)
    if hasattr(target, 'evaluacion_id'):
        evaluacion = get_evaluacion_by_id(target.evaluacion_id)
        return obtener_curso_id_from_evaluacion(evaluacion) if evaluacion else None
    return None

def obtener_curso_id_from_seccion(target, seccion_attr):
    if hasattr(target, 'seccion') and target.seccion:
        return target.seccion.curso_id
    if hasattr(target, seccion_attr):
        seccion = get_seccion_by_id(session, getattr(target, seccion_attr))
        return seccion.curso_id if seccion else None
    return None

def register_events():
    models = [Seccion, Categoria, Evaluacion, Notas, AlumnoSeccion, ProfesorSeccion]
    for model in models:
        event.listen(model, 'before_insert', verificar_curso_abierto)
        event.listen(model, 'before_update', verificar_curso_abierto)
        event.listen(model, 'before_delete', verificar_curso_abierto)
    
    print("Eventos SQLAlchemy para verificar cursos cerrados registrados correctamente")