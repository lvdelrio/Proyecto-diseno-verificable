from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..config import db

class AlumnoSeccion(db.Model):
    __tablename__ = "alumno_seccion"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_alumno: Mapped[int] = mapped_column(Integer, ForeignKey("alumnos.id"), nullable=False)
    id_seccion: Mapped[int] = mapped_column(Integer, ForeignKey("secciones.id"), nullable=False)

    alumno: Mapped["Alumno"] = relationship("Alumno", back_populates="secciones_alumno")
    seccion: Mapped["Seccion"] = relationship("Seccion", back_populates="alumnos_seccion")

    def __repr__(self):
        return f"<AlumnoSeccion(id={self.id}, id_alumno={self.id_alumno}, id_seccion={self.id_seccion})>"
