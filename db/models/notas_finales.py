from ..config import db
from sqlalchemy import Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
class NotasFinales(db.Model):
    __tablename__ = 'notas_finales'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nota_final: Mapped[float] = mapped_column(Float, nullable=False)
    curso_id: Mapped[int] = mapped_column(Integer, ForeignKey("cursos.id"), nullable=True)
    alumno_id: Mapped[int] = mapped_column(Integer, ForeignKey("alumnos.id"), nullable=False)

    curso: Mapped["Curso"] = relationship("Curso", back_populates="notas_finales")
    alumno: Mapped["Alumno"] = relationship("Alumno", back_populates="notas_finales")

    def __repr__(self):
        return f"<Curso(id={self.id}, nombre='{self.nombre}')>"