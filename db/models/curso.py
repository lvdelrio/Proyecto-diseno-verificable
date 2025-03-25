from ..config import db
class Curso(db.Model):
    __tablename__ = 'cursos'  # Name of the table in the database

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    nombre = db.Column(db.String(100), nullable=False)  # Course name
    descripcion = db.Column(db.Text, nullable=True)  # Course description

    def __repr__(self):
        return f"<Curso(id={self.id}, nombre='{self.nombre}')>"