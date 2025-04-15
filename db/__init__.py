from .config import db, init_db
from .models.alumno import Alumno
from .models.curso import Curso
from .models.notas import Notas
from .models.evaluacion import Evaluacion
from .models.seccion import Seccion
from .models.profesor import Profesor
from .models.requisitos import CursoRequisito
from .models.categoria import Categoria
from .models.alumno_seccion import AlumnoSeccion

__all__ = ['db', 'init_db', 'Curso', 'Alumno', 'Notas', 'Evaluacion', 'Seccion', 'Profesor', 'CursoRequisito', 'Categoria', 'AlumnoSeccion']
