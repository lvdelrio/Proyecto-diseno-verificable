from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.config import db

class Curso(db.Model):
    __tablename__ = 'cursos'

    id = db.Column(db.Integer, primary_key=True)
    fecha_impartida = db.Column(db.Integer, nullable=False)
    semestre_impartido = db.Column(db.String(100), nullable=False)
    tipo_curso_id: Mapped[int] = mapped_column(Integer, ForeignKey("tipo_cursos.id"), nullable=True)
    cerrado = db.Column(db.Boolean, default=False, nullable=False)

    tipo_curso: Mapped["TipoCurso"] = relationship(back_populates="cursos")
    secciones = db.relationship("Seccion", back_populates="curso", cascade="all, delete-orphan")
    notas_finales = db.relationship("NotasFinales",
                                    back_populates="curso",
                                    cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Curso(id={self.id}, codigo='{self.tipo_curso.codigo}')>"
