from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.config import db

class AlumnoSeccion(db.Model):
    __tablename__ = "alumno_seccion"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    alumno_id: Mapped[int] = mapped_column(Integer,
                                           ForeignKey("alumnos.id", ondelete="CASCADE"),
                                           nullable=False)
    seccion_id: Mapped[int] = mapped_column(Integer,
                                            ForeignKey("secciones.id", ondelete="CASCADE"),
                                            nullable=False)

    alumno: Mapped["Alumno"] = relationship("Alumno", overlaps="alumnos,secciones")
    seccion: Mapped["Seccion"] = relationship("Seccion", overlaps="alumnos,secciones")

    def __repr__(self):
        return (
            f"<AlumnoSeccion(id={self.id}, id_alumno={self.id_alumno}, "
            f"seccion_id={self.seccion_id})>"
        )
