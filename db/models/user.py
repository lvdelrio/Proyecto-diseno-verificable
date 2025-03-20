from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from  ..config import db
from sqlalchemy import DateTime

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(Integer, primary_key=True, index=True)
    name = db.Column(String(50), index=True)
    email = db.Column(String(50), unique=True, index=True)
    fecha_ingreso = db.Column(DateTime)