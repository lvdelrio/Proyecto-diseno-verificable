from .config import db, init_db
from .models.alumno import Alumno
from .models.curso import Curso
from .models.profesor import Profesor

__all__ = ['db', 'init_db', 'Curso', 'Alumno', 'Profesor']