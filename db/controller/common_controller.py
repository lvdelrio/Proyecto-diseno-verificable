from flask import abort
from sqlalchemy.orm import Session
from ..models.seccion import Seccion
from ..models.profesor import Profesor
from ..models.alumno_seccion import AlumnoSeccion
from ..models.evaluacion import Evaluacion
from ..models.curso import Curso
from ..models.categoria import Categoria
from ..models.notas import Notas
from ..models.profesor_seccion import ProfesorSeccion
from ..models.categoria import Categoria
from ..controller.curso_controller import get_curso_by_id

def get_seccion_by_id(db: Session, new_seccion: int):
    return db.query(Seccion).filter(Seccion.id == new_seccion).first()

def get_profesor_by_id(db: Session, profesor_id: int):
    return db.query(Profesor).filter(Profesor.id == profesor_id).first()

def get_all_alumno_seccion_by_categoria_id(db: Session, categoria_id: int):
    return db.query(AlumnoSeccion).filter(AlumnoSeccion.categoria_id == categoria_id).all()

def get_evaluaciones_by_categoria_id(db: Session, categoria_id: int):
    return db.query(Evaluacion).filter(Evaluacion.categoria_id == categoria_id).all()

def get_categorias_by_seccion_id(db: Session, seccion_id: int):
    return db.query(Categoria).filter(Categoria.seccion_id == seccion_id).all()
