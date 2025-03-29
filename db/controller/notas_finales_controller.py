from sqlalchemy.orm import Session
from db.models.alumno import Alumno
from db.models.notas_finales import NotasFinales


def create_nota_final(db: Session, alumno_id: int, nota_final: float):
    alumno = db.query(Alumno).filter(Alumno.id == alumno_id).first()
    if not alumno:
        return None
    
    new_nota_final = NotasFinales(nota_final=nota_final, alumno=alumno)
    db.add(new_nota_final)
    db.commit()
    db.refresh(new_nota_final)
    print(f"Nota final creada: {new_nota_final.nota_final} para el alumno: {alumno.nombre}")
    return new_nota_final