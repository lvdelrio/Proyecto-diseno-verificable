from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from  ..config import db
from sqlalchemy import DateTime

class Alumno(db.Model):
    __tablename__ = "alumnos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(50), index=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    fecha_ingreso: Mapped[DateTime] = mapped_column(DateTime)

    notas: Mapped[list["Notas"]] = relationship("Notas", back_populates="alumno")
    notas_finales: Mapped[list["NotasFinales"]] = relationship("NotasFinales", back_populates="alumno")
    secciones: Mapped[list["Seccion"]] = relationship(
                                            "Seccion",
                                            secondary="alumno_seccion"
                                            )
    alumnos_seccion: Mapped[list["AlumnoSeccion"]] = relationship(
        "AlumnoSeccion",
        back_populates="alumno",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<Alumno(id={self.id}, nombre='{self.nombre}')>"