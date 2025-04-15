from sqlalchemy.orm import Session
from db.models.evaluacion import Evaluacion
from datetime import datetime

def create_evaluacion(db: Session, tipo: int, ponderacion: float, opcional: bool, seccion_id: int = None):
    nueva_evaluacion = Evaluacion(
        tipo=tipo,
        ponderacion=ponderacion,
        opcional=int(opcional),
        seccion_id=seccion_id
    )
    db.add(nueva_evaluacion)
    db.commit()
    db.refresh(nueva_evaluacion)
    return nueva_evaluacion

def get_evaluacion_by_id(db: Session, evaluacion_id: int):
    return db.query(Evaluacion).filter(Evaluacion.id == evaluacion_id).first()

def get_all_evaluaciones(db: Session):
    return db.query(Evaluacion).all()

def get_evaluaciones_by_seccion(db: Session, seccion_id: int):
    return db.query(Evaluacion).filter(Evaluacion.seccion_id == seccion_id).all()

def update_evaluacion(db: Session, evaluacion_id: int, **kwargs):
    evaluacion = db.query(Evaluacion).filter(Evaluacion.id == evaluacion_id).first()
    if evaluacion:
        for key, value in kwargs.items():
            if hasattr(evaluacion, key):
                setattr(evaluacion, key, value)
        db.commit()
        db.refresh(evaluacion)
    return evaluacion

def delete_evaluacion(db: Session, evaluacion_id: int):
    evaluacion = db.query(Evaluacion).filter(Evaluacion.id == evaluacion_id).first()
    if evaluacion:
        db.delete(evaluacion)
        db.commit()
        return True
    return False