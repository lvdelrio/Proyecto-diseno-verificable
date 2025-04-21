from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..config import db

class Seccion(db.Model):
    __tablename__ = "secciones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(50))
    curso_id: Mapped[int] = mapped_column(Integer, ForeignKey("cursos.id", ondelete="CASCADE"), nullable=True)
    sala_id: Mapped[int] = mapped_column(Integer, ForeignKey("salas.id", ondelete="SET NULL"), nullable=True)

    curso: Mapped["Curso"] = relationship(back_populates="secciones")
    categorias: Mapped[list["Categoria"]] = relationship("Categoria", back_populates="seccion", cascade="all, delete-orphan")
    alumnos: Mapped[list["Alumno"]] = relationship(
                                                "Alumno",
                                                secondary="alumno_seccion",
                                                back_populates="secciones"
                                            )
    profesores: Mapped[list["Profesor"]] = relationship(
                                                "Profesor",
                                                secondary="profesor_seccion",
                                                back_populates="secciones"
                                            )
    alumnos_seccion: Mapped[list["AlumnoSeccion"]] = relationship(
        "AlumnoSeccion",
        back_populates="seccion",
        cascade="all, delete-orphan"
    )
    sala: Mapped["Sala"] = relationship("Sala", back_populates="secciones")

