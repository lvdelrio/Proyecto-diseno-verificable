from sqlalchemy.orm import Session
from db.models.notas import Notas
from db.models.alumno import Alumno
from db.models.evaluacion import Evaluacion
import traceback

INDEX = 1

def create_nota(db: Session, alumno_id: int, evaluacion_id: int, nota: float):
    nota_existente = db.query(Notas).filter(
        Notas.alumno_id == alumno_id,
        Notas.evaluacion_id == evaluacion_id
    ).first()
    if nota_existente:
        nota_existente.nota = nota
    else:
        nueva_nota = Notas(
            alumno_id=alumno_id,
            evaluacion_id=evaluacion_id,
            nota=nota
        )
        db.add(nueva_nota)
    db.commit()
    return nota_existente if nota_existente else nueva_nota

def get_all_notas(db: Session):
    return db.query(Notas).all()

def get_nota_by_id(db: Session, nota_id: int):
    return db.query(Notas).filter(Notas.id == nota_id).first()

def get_nota(db: Session, alumno_id: int, evaluacion_id: int):
    return db.query(Notas).filter(
        Notas.alumno_id == alumno_id,
        Notas.evaluacion_id == evaluacion_id
    ).first()

def get_notas_by_alumno(db: Session, alumno_id: int):
    return db.query(Notas).filter(Notas.alumno_id == alumno_id).all()

def get_notas_by_evaluacion(db: Session, evaluacion_id: int):
    return db.query(Notas).filter(Notas.evaluacion_id == evaluacion_id).all()

def update_nota(db: Session, nota_id: int, nueva_nota: float):
    nota = get_nota_by_id(db, nota_id)
    if nota:
        nota.nota = nueva_nota
        db.commit()
        return nota
    return None


def delete_nota(db: Session, nota_id: int):
    nota = get_nota_by_id(db, nota_id)
    if nota:
        db.delete(nota)
        db.commit()
        return True
    return False

def get_evaluaciones_by_categoria(db: Session, categoria_id: int):
    return db.query(Evaluacion).filter(
        Evaluacion.categoria_id == categoria_id
    ).all()

def extract_number_from_name(evaluacion):
    nombre_evaluacion = evaluacion.nombre
    last_digit = nombre_evaluacion.split()[-INDEX]
    if last_digit.isdigit():
        return int(last_digit)
    return 0

def get_evaluacion_by_instancia(evaluaciones, instancia):
    evaluaciones_sorted = sorted(evaluaciones, key=extract_number_from_name)
    return evaluaciones_sorted[instancia - INDEX]

def load_notas_from_json(db: Session, data: dict):
    notas_data = data.get("notas", [])
    for nota_data in notas_data:
        alumno_id = nota_data.get("alumno_id")
        categoria_id = nota_data.get("topico_id")
        evaluacion_id = nota_data.get("instancia")  
        nota_valor = nota_data.get("nota")
        evaluaciones = get_evaluaciones_by_categoria(db, categoria_id)
        evaluacion = get_evaluacion_by_instancia(evaluaciones, evaluacion_id)
        try:
            create_nota(db, alumno_id, evaluacion.id, float(nota_valor))
        except Exception as e:
            db.rollback()   
    