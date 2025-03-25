from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from  ..config import db
from sqlalchemy import DateTime

class Alumno(db.Model):
    __tablename__ = "alumnos"

    id = db.Column(Integer, primary_key=True, index=True)
    nombre = db.Column(String(50), index=True)
    email = db.Column(String(50), unique=True, index=True)
    fecha_ingreso = db.Column(DateTime)

    def __repr__(self):
        return f"<Alumno(id={self.id}, nombre='{self.nombre}')>"