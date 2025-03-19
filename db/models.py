from .config import db

class Course(db.Model):
    __tablename__ = 'courses'  # Name of the table in the database

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    name = db.Column(db.String(100), nullable=False)  # Course name
    description = db.Column(db.Text, nullable=True)  # Course description

    def __repr__(self):
        return f"<Course(id={self.id}, name='{self.name}')>"