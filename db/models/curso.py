from ..config import db
class Curso(db.Model):
    __tablename__ = 'cursos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)

    secciones = db.relationship("Seccion", back_populates="curso")

    def __repr__(self):
        return f"<Curso(id={self.id}, nombre='{self.nombre}')>"