from ..config import db
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column

class Curso(db.Model):
    __tablename__ = 'cursos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    semestre_de_ejecucion = db.Column(db.String(100), nullable=False)
    
    secciones = db.relationship("Seccion", back_populates="curso")
    requisitos = relationship(
        "CursoRequisito",
        foreign_keys='CursoRequisito.curso_id',
        back_populates="curso",
        cascade="all, delete-orphan"
    )

    notas_finales = db.relationship("NotasFinales", back_populates="curso")

    def __repr__(self):
        return f"<Curso(id={self.id}, nombre='{self.nombre}')>"