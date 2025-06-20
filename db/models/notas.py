from sqlalchemy import Integer, ForeignKey, Float
from sqlalchemy.orm import relationship, Mapped
from db.config import db

class Notas(db.Model):
    __tablename__ = "notas"

    id = db.Column(Integer, primary_key=True, index=True)
    alumno_id = db.Column(Integer, ForeignKey("alumnos.id"), nullable=True)
    evaluacion_id = db.Column(Integer, ForeignKey("evaluaciones.id"), nullable=True)
    nota = db.Column(Float)
    alumno: Mapped["Alumno"] = relationship(back_populates="notas")
    evaluacion: Mapped["Evaluacion"] = relationship("Evaluacion", back_populates="notas")
