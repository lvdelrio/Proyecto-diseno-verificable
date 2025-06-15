from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.config import db

class ProfesorSeccion(db.Model):
    __tablename__ = "profesor_seccion"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profesor_id: Mapped[int] = mapped_column(Integer, ForeignKey("profesores.id"), nullable=False)
    seccion_id: Mapped[int] = mapped_column(Integer, ForeignKey("secciones.id"), nullable=False)

    profesor: Mapped["Profesor"] = relationship("Profesor")
    seccion: Mapped["Seccion"] = relationship("Seccion")

    def __repr__(self):
        return (
            f"<ProfesorSeccion(id={self.id}, "
            f"id_profesor={self.id_profesor}, "
            f"seccion_id={self.seccion_id})>"
        )
