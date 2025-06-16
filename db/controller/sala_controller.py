from sqlalchemy.orm import Session
from flask import flash
from db.models.salas import Sala

def create_sala(db: Session, nombre: str, capacidad: int):
    sala = Sala(nombre=nombre, capacidad=capacidad)
    db.add(sala)
    db.commit()
    db.refresh(sala)
    return sala

def get_all_salas(db: Session):
    return db.query(Sala).all()

def get_sala_by_id(db: Session, sala_id: int):
    return db.query(Sala).filter(Sala.id == sala_id).first()

def delete_sala(db: Session, sala_id: int):
    sala = get_sala_by_id(db, sala_id)
    if sala:
        db.delete(sala)
        db.commit()
        return True
    return False

def edit_sala_by_id(db: Session, sala_id: int, nombre: str, capacidad: int):
    sala = get_sala_by_id(db, sala_id)
    if sala:
        sala.nombre = nombre
        sala.capacidad = capacidad
        db.commit()
        db.refresh(sala)
        return sala
    return None

def load_salas_from_json(db: Session, data: dict):
    sala_data = data.get("salas", [])
    if not sala_data:
        flash("No se encontraron salas para cargar en el JSON proporcionado.", "error")
        return
    for sala in sala_data:
        create_sala(
            db,
            nombre=sala.get("nombre"),
            capacidad=sala.get("capacidad")
        )
