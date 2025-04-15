from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..config import db

class Seccion(db.Model):
    __tablename__ = "secciones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(50))
    curso_id: Mapped[int] = mapped_column(Integer, ForeignKey("cursos.id"), nullable=True)

    curso: Mapped["Curso"] = relationship(back_populates="secciones")
    categorias: Mapped[list["Categoria"]] = relationship("Categoria", back_populates="seccion")
    alumnos: Mapped[list["Alumno"]] = relationship(
                                                "Alumno",
                                                secondary="alumno_seccion",
                                                back_populates="secciones"
                                            )
    profesores: Mapped[list["Profesor"]] = relationship(
                                                "Profesor",
                                                secondary="profesor_seccion",
                                                back_populates="profesores"
                                            )

