from sqlalchemy.orm import Session
from ..models.seccion import Seccion
from ..models.profesor import Profesor
from ..models.alumno_seccion import AlumnoSeccion
from ..models.evaluacion import Evaluacion
from ..models.curso import Curso
from ..models.categoria import Categoria
from ..models.notas import Notas
from ..models.profesor_seccion import ProfesorSeccion
from flask import abort
from ..models.categoria import Categoria

def get_seccion_by_id(db: Session, new_seccion: int):
    return db.query(Seccion).filter(Seccion.id == new_seccion).first()

def get_profesor_by_id(db: Session, profesor_id: int):
    return db.query(Profesor).filter(Profesor.id == profesor_id).first()

def get_alumno_seccion_by_id(db: Session, alumno_seccion_id: int):
    return db.query(AlumnoSeccion).filter(AlumnoSeccion.id == alumno_seccion_id).first()

def get_all_alumno_seccion_by_categoria_id(db: Session, categoria_id: int):
    return db.query(AlumnoSeccion).filter(AlumnoSeccion.categoria_id == categoria_id).all()

def get_evaluaciones_by_categoria_id(db: Session, categoria_id: int):
    return db.query(Evaluacion).filter(Evaluacion.categoria_id == categoria_id).all()

def get_categorias_by_seccion_id(db: Session, seccion_id: int):
    return db.query(Categoria).filter(Categoria.seccion_id == seccion_id).all()

def check_curso_abierto(db: Session, curso_id=None, tipo_objeto=None, objeto_id=None):
    if curso_id is None:
        if tipo_objeto is None or objeto_id is None:
            abort(400, description="Información insuficiente para verificar el estado del curso")
        curso_id = _determinar_curso_id(db, tipo_objeto, objeto_id)
    
    if curso_id is None:
        abort(404, description="No se pudo determinar el curso asociado")
    
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        abort(404, description="Curso no encontrado")
    
    if curso.cerrado:
        abort(403, description="El curso está cerrado y ya no se puede modificar")
    
    return True

def _determinar_curso_id(db: Session, tipo_objeto: str, objeto_id: int):
    tipo = tipo_objeto.lower()
    print(f"FUNCION NUEVA: Tipo de objeto: {tipo}")
    curso_id = None
    
    if tipo == 'seccion':
        seccion = db.query(Seccion).filter(Seccion.id == objeto_id).first()
        curso_id = seccion.curso_id if seccion else None
        
    elif tipo == 'alumno':
        alumno_seccion = db.query(AlumnoSeccion).filter(AlumnoSeccion.alumno_id == objeto_id).first()
        curso_id = alumno_seccion.seccion.curso_id if alumno_seccion and alumno_seccion.seccion else None
        
    elif tipo == 'profesor':
        profesor_seccion = db.query(ProfesorSeccion).filter(ProfesorSeccion.profesor_id == objeto_id).first()
        curso_id = profesor_seccion.seccion.curso_id if profesor_seccion and profesor_seccion.seccion else None
        
    elif tipo == 'categoria':
        categoria = db.query(Categoria).filter(Categoria.id == objeto_id).first()
        curso_id = categoria.seccion.curso_id if categoria and hasattr(categoria, 'seccion') else None
        
    elif tipo == 'evaluacion':
        evaluacion = db.query(Evaluacion).filter(Evaluacion.id == objeto_id).first()
        if evaluacion and evaluacion.categoria and hasattr(evaluacion.categoria, 'seccion'):
            curso_id = evaluacion.categoria.seccion.curso_id
            
    elif tipo == 'nota':
        nota = db.query(Notas).filter(Notas.id == objeto_id).first()
        if nota and nota.evaluacion and nota.evaluacion.categoria:
            categoria = nota.evaluacion.categoria
            if hasattr(categoria, 'seccion'):
                curso_id = categoria.seccion.curso_id
    return curso_id