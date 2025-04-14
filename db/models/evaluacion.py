from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, Mapped
from  ..config import db
from sqlalchemy import DateTime

class Evaluacion(db.Model):
    __tablename__ = "evaluaciones"

    id = db.Column(Integer, primary_key=True, index=True)
    tipo = db.Column(Integer, index=True)
    ponderacion = db.Column(Float, index=True)
    opcional = db.Column(Integer, index=True)
    categoria_id = db.Column(Integer, ForeignKey("categoria.id"), nullable = True)
    
    categoria: Mapped["Categoria"] = relationship("Categoria", back_populates="evaluaciones")
    notas: Mapped[list["Notas"]] = relationship("Notas", back_populates="evaluacion")
