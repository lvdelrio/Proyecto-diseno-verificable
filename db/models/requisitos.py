from ..config import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
class CursoRequisito(db.Model):
    __tablename__ = 'cursos_requisitos'

    id = db.Column(db.Integer, primary_key=True)
    curso_id: Mapped[int] = mapped_column(Integer, ForeignKey('cursos.id'), nullable=False)
    curso_requisito_id: Mapped[int] = mapped_column(Integer, ForeignKey('cursos.id'), nullable=False)

    curso: Mapped["Curso"] = relationship(
        "Curso", foreign_keys=[curso_id], back_populates="requisitos"
    )
    curso_requisito = relationship(
        "Curso",
        foreign_keys=[curso_requisito_id]
    )

    def __repr__(self):
          return f"<CursoRequisito(curso_id={self.curso_id}, curso_requisito_id={self.curso_requisito_id})>"