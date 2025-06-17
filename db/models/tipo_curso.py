from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import relationship, mapped_column, Mapped
from db.config import db
from db.utils.models_variables import DELETE_CASCADE

class TipoCurso(db.Model):
    __tablename__ = 'tipo_cursos'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    codigo: Mapped[str] = mapped_column(String(20), nullable=True)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    creditos: Mapped[int] = mapped_column(Integer, nullable=False)

    cursos = relationship("Curso", back_populates="tipo_curso", cascade=DELETE_CASCADE)

    requisitos = relationship(
        "CursoRequisito",
        foreign_keys='CursoRequisito.tipo_curso_id',
        back_populates="tipo_curso",
        cascade=DELETE_CASCADE
    )
    requerido_por = relationship(
        "CursoRequisito",
        foreign_keys='CursoRequisito.curso_requisito_id',
        back_populates="curso_requisito",
        cascade=DELETE_CASCADE
    )

    def __repr__(self):
        return f"<Tipo de curso(id={self.id}, codigo='{self.codigo}')>"
