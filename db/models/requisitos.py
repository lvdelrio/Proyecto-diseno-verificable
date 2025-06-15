from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer
from db.config import db

class CursoRequisito(db.Model):
    __tablename__ = 'cursos_requisitos'

    id = db.Column(db.Integer, primary_key=True)
    tipo_curso_id: Mapped[int] = mapped_column(
        Integer,
        db.ForeignKey('tipo_cursos.id'),
        nullable=False
    )
    curso_requisito_id: Mapped[int] = mapped_column(
         Integer,
         db.ForeignKey('tipo_cursos.id'),
         nullable=False
    )

    tipo_curso = relationship(
        "TipoCurso", foreign_keys=[tipo_curso_id], back_populates="requisitos"
    )
    curso_requisito = relationship(
        "TipoCurso", foreign_keys=[curso_requisito_id], back_populates="requerido_por"
    )

    def __repr__(self):
        return f"<CursoRequisito(tipo_curso_id={self.tipo_curso_id}, curso_requisito_id={self.curso_requisito_id})>"
