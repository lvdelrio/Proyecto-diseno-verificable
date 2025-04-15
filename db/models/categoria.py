from sqlalchemy import Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..config import db

class Categoria(db.Model):
    __tablename__ = "categoria"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tipo_categoria: Mapped[str] = mapped_column(String(20), nullable=False)
    id_seccion: Mapped[int] = mapped_column(Integer, ForeignKey("secciones.id"), nullable=False)
    ponderacion: Mapped[float] = mapped_column(Float, nullable=False)
    opcional: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    seccion: Mapped["Seccion"] = relationship("Seccion", back_populates="categorias")
    evaluaciones: Mapped[list["Evaluacion"]] = relationship("Evaluacion", back_populates="categoria")

    def __repr__(self):
        return (f"<Categoria (id={self.id}, tipo_categoria='{self.tipo_categoria}', "
                f"id_seccion={self.id_seccion})>")
