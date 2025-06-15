from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.config import db

class Sala(db.Model):
    __tablename__ = 'salas'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(20), nullable=False)
    capacidad: Mapped[int] = mapped_column(Integer, nullable=False)

    secciones:  Mapped[list["Seccion"]] = relationship("Seccion", back_populates="sala")

    def __repr__(self):
        return f"<Sala(id={self.id}, nombre='{self.nombre}, capacidad='{self.capacidad}')>"
