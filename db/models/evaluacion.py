from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship, Mapped
from  ..config import db
from sqlalchemy import DateTime

class Evaluacion(db.Model):
    __tablename__ = "evaluaciones"

    id = db.Column(Integer, primary_key=True, index=True)
    nombre = db.Column(String(20), index=True)
    ponderacion = db.Column(Float, index=True)
    opcional = db.Column(Integer, index=True)
    categoria_id = db.Column(Integer, ForeignKey("categoria.id"), nullable = True)
    tipo_ponderacion = db.Column(Boolean)
    
    categoria: Mapped["Categoria"] = relationship("Categoria", back_populates="evaluaciones")
    notas: Mapped[list["Notas"]] = relationship("Notas", back_populates="evaluacion")
