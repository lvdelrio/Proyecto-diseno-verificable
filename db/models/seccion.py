from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from  ..config import db

class Seccion(db.Model):
    __tablename__ = "secciones"

    id = db.Column(Integer, primary_key=True, index=True)
    nombre = db.Column(String(50))
    curso_id = db.Column(Integer, ForeignKey("cursos.id"), nullable=True)

    curso: Mapped["Curso"] = relationship( back_populates="secciones")
    evaluacion: Mapped[list["Evaluacion"]] = relationship("Evaluacion" ,back_populates="seccion")