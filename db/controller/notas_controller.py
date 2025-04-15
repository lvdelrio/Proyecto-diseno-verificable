from sqlalchemy.orm import Session
from db.models.notas import Notas
from db.models.alumno import Alumno
from db.models.evaluacion import Evaluacion

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

def get_nota(db: Session, alumno_id: int, evaluacion_id: int):
    return db.query(Notas).filter(
        Notas.alumno_id == alumno_id,
        Notas.evaluacion_id == evaluacion_id
    ).first()

def get_notas_by_alumno(db: Session, alumno_id: int):
    return db.query(Notas).filter(Notas.alumno_id == alumno_id).all()

def get_notas_by_evaluacion(db: Session, evaluacion_id: int):
    return db.query(Notas).filter(Notas.evaluacion_id == evaluacion_id).all()

def delete_nota(db: Session, nota_id: int):
    nota = db.query(Notas).filter(Notas.id == nota_id).first()
    if nota:
        db.delete(nota)
        db.commit()
        return True
    return False

def calculate_promedio_alumno(db: Session, alumno_id: int):
    notas = db.query(Notas).join(Evaluacion).filter(
        Notas.alumno_id == alumno_id
    ).all()
    
    if not notas:
        return None
        
    total_ponderado = sum(nota.nota * nota.evaluacion.ponderacion for nota in notas)
    total_ponderacion = sum(nota.evaluacion.ponderacion for nota in notas)
    
    return total_ponderado / total_ponderacion if total_ponderacion else 0