from ..config import db
from ..models.alumno_seccion import AlumnoSeccion

def agregar_alumno_seccion(id_alumno, id_seccion):
    nuevo_registro = AlumnoSeccion(id_alumno=id_alumno, id_seccion=id_seccion)
    db.session.add(nuevo_registro)
    db.session.commit()
    return nuevo_registro

def obtener_alumno_seccion(id):
    return AlumnoSeccion.query.get(id)

def eliminar_alumno_seccion(id):
    registro = AlumnoSeccion.query.get(id)
    db.session.delete(registro)
    db.session.commit()
