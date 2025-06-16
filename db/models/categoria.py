from sqlalchemy import Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.config import db

class Categoria(db.Model):
    __tablename__ = "categoria"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tipo_categoria: Mapped[str] = mapped_column(String(20), nullable=False)
    seccion_id: Mapped[int] = mapped_column(Integer, ForeignKey("secciones.id"), nullable=False)
    ponderacion: Mapped[float] = mapped_column(Float, nullable=False)
    tipo_ponderacion: Mapped[bool] = mapped_column(Boolean, default=False)

    seccion: Mapped["Seccion"] = relationship("Seccion", back_populates="categorias")
    evaluaciones: Mapped[list["Evaluacion"]] = relationship("Evaluacion",
                                                            back_populates="categoria",
                                                            cascade="all, delete-orphan")

    def __repr__(self):
        return (f"<Categoria (id={self.id}, tipo_categoria='{self.tipo_categoria}', "
                f"seccion_id={self.seccion_id})>")
