from ..config import db
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship, mapped_column, Mapped

class TipoCurso(db.Model):
    __tablename__ = 'tipo_cursos'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(20), nullable=True)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    codigo: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    creditos: Mapped[int] = mapped_column(Integer, nullable=False)

    cursos = relationship("Curso", back_populates="tipo_curso", cascade="all, delete-orphan")

    requisitos = relationship(
        "CursoRequisito",
        foreign_keys='CursoRequisito.tipo_curso_id',
        back_populates="tipo_curso",
        cascade="all, delete-orphan"
    )
    requerido_por = relationship(
        "CursoRequisito",
        foreign_keys='CursoRequisito.curso_requisito_id',
        back_populates="curso_requisito",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Tipo de curso(id={self.id}, nombre='{self.nombre}')>"