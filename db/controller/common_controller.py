from flask import abort
from sqlalchemy.orm import Session
from db.models.tipo_curso import TipoCurso
from db.models.curso import Curso
from db.models.seccion import Seccion
from db.models.profesor import Profesor
from db.models.alumno_seccion import AlumnoSeccion
from db.models.alumno import Alumno
from db.models.evaluacion import Evaluacion
from db.models.categoria import Categoria
from db.models.notas import Notas
from db.models.notas_finales import NotasFinales

def get_seccion_by_id(db: Session, new_seccion: int):
    return db.query(Seccion).filter(Seccion.id == new_seccion).first()

def get_alumno_by_id(db: Session, user_id: int):
    return db.query(Alumno).filter(Alumno.id == user_id).first()

def get_profesor_by_id(db: Session, profesor_id: int):
    return db.query(Profesor).filter(Profesor.id == profesor_id).first()

def get_all_alumno_seccion_by_categoria_id(db: Session, categoria_id: int):
    return db.query(AlumnoSeccion).filter(AlumnoSeccion.categoria_id == categoria_id).all()

def get_all_alumno__by_categoria_id(db: Session, categoria_id: int):
    seccion_id = db.query(Categoria).filter(Categoria.id == categoria_id).first().seccion_id
    seccion = get_seccion_by_id(db, seccion_id)
    return seccion.alumnos

def get_evaluaciones_by_categoria_id(db: Session, categoria_id: int):
    return db.query(Evaluacion).filter(Evaluacion.categoria_id == categoria_id).all()

def get_categorias_by_seccion_id(db: Session, seccion_id: int):
    return db.query(Categoria).filter(Categoria.seccion_id == seccion_id).all()

def get_notas_by_evaluacion_id(db: Session, evaluacion_id: int):
    return db.query(Notas).filter(Notas.evaluacion_id == evaluacion_id).all()

def get_notas_finales_by_seccion_id(db: Session, seccion_id: int):
    return (
        db.query(NotasFinales)
        .join(Curso, Curso.id == NotasFinales.curso_id)
        .join(Seccion, Seccion.curso_id == Curso.id)
        .filter(Seccion.id == seccion_id)
        .all()
    )

def get_alumno_report_data_by_alumno_id(db: Session, alumno_id: int):
    return (
        db.query(
            TipoCurso.codigo,
            Seccion.nombre,
            NotasFinales.nota_final,
            Curso.fecha_impartida,
            Curso.semestre_impartido,
        )
        .select_from(Alumno)
        .join(AlumnoSeccion, AlumnoSeccion.alumno_id == Alumno.id)
        .join(Seccion, Seccion.id == AlumnoSeccion.seccion_id)
        .join(Curso, Curso.id == Seccion.curso_id)
        .join(TipoCurso, TipoCurso.id == Curso.tipo_curso_id)
        .join(NotasFinales, (NotasFinales.curso_id == Curso.id) & (NotasFinales.alumno_id == Alumno.id))
        .filter(Alumno.id == alumno_id)
        .filter(Curso.cerrado == True)
        .distinct()
        .all()
    )