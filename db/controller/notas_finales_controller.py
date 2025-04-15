from sqlalchemy.orm import Session
from db.models.alumno import Alumno
from db.controller.alumno_controller import get_alumno_by_id
from db.models.notas_finales import NotasFinales
#TODO: AGREGAR EL CREATE NOTA FINAL PARA EL FRONTEND
def create_nota_final(db: Session, alumno_id: int, nota_final: float):
    alumno = get_alumno_by_id(db, alumno_id)
    if not alumno:
        return None
    
    new_nota_final = NotasFinales(nota_final=nota_final, alumno=alumno)
    db.add(new_nota_final)
    db.commit()
    db.refresh(new_nota_final)
    print(f"Nota final creada: {new_nota_final.nota_final} para el alumno: {alumno.nombre}")
    return new_nota_final

def create_or_update_nota_final(db: Session, alumno_id: int, curso_id: int, nota_final: float):
    """
    Crea o actualiza una nota final
    """
    nota_existente = db.query(NotasFinales).filter(
        NotasFinales.alumno_id == alumno_id,
        NotasFinales.curso_id == curso_id
    ).first()
    
    if nota_existente:
        nota_existente.nota_final = nota_final
    else:
        nueva_nota = NotasFinales(
            alumno_id=alumno_id,
            curso_id=curso_id,
            nota_final=nota_final
        )
        db.add(nueva_nota)
    
    db.commit()
    return nota_existente if nota_existente else nueva_nota

def get_nota_final(db: Session, alumno_id: int, curso_id: int):
    """
    Obtiene una nota final específica
    """
    return db.query(NotasFinales).filter(
        NotasFinales.alumno_id == alumno_id,
        NotasFinales.curso_id == curso_id
    ).first()

def get_notas_finales_by_alumno(db: Session, alumno_id: int):
    """
    Obtiene todas las notas finales de un alumno
    """
    return db.query(NotasFinales).filter(
        NotasFinales.alumno_id == alumno_id
    ).all()

def get_notas_finales_by_curso(db: Session, curso_id: int):
    """
    Obtiene todas las notas finales de un curso
    """
    return db.query(NotasFinales).filter(
        NotasFinales.curso_id == curso_id
    ).all()

def calcular_nota_final(db: Session, alumno_id: int, curso_id: int):
    """
    Calcula automáticamente la nota final basada en las evaluaciones
    """
    from .notas_controller import calcular_promedio_alumno
    promedio = calcular_promedio_alumno(db, alumno_id)
    if promedio is not None:
        return create_or_update_nota_final(db, alumno_id, curso_id, promedio)
    return None