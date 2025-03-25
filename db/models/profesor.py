from ..config import db
class Profesor(db.Model):
    __tablename__ = 'profesores'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Profesor(id={self.id}, email='{self.nombre}')>"