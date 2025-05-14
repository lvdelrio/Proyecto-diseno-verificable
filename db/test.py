
from db.config import db
from db.models.tipo_curso import TipoCurso
from db.models.requisitos import CursoRequisito
from db.models.curso import Curso
from db.models.seccion import Seccion
from db.models.profesor import Profesor
from db.models.alumno import Alumno
from db.models.profesor_seccion import ProfesorSeccion
from db.models.alumno_seccion import AlumnoSeccion
from db.models.categoria import Categoria
from db.models.evaluacion import Evaluacion
from db.models.notas import Notas
from db.models.notas_finales import NotasFinales
from db.models.salas import Sala


def reset_database(session):
    try:
        session.query(ProfesorSeccion).delete()
        session.query(AlumnoSeccion).delete()
        session.query(NotasFinales).delete()
        session.query(Notas).delete()
        session.query(Evaluacion).delete()
        session.query(Categoria).delete()

        session.query(Seccion).delete()
        session.query(Curso).delete()
        session.query(Sala).delete()
        session.query(Profesor).delete()
        session.query(Alumno).delete()
        session.query(CursoRequisito).delete()
        session.query(TipoCurso).delete()

        session.commit()
        return {"status": "ok", "message": "Database reset successful."}
    except Exception as e:
        session.rollback()
        return {"status": "error", "message": str(e)}