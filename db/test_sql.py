
from db.config import db
from db.models.alumno import Alumno
from db.models.notas import Notas
from db.models.evaluacion import Evaluacion
def test_sql():
    session = db.session

    alumno = session.query(Alumno).filter(Alumno.id == 1).first()
    evaluacion = session.query(Evaluacion).filter(Evaluacion.id == 1).first()

    print("Alumno:", alumno)
    print("Evaluacion:", evaluacion)

    nota = Notas(nota=6.5, alumno=alumno)

    session.add(nota)
    session.commit()

    print(f"Nota creada: {nota.id}, valor: {nota.nota}")
    alumno_con_notas = session.query(Alumno).filter(Alumno.id == 1).first()
    print("Notas del Alumno:")
    for n in alumno_con_notas.notas:
        print(f" - Nota ID: {n.id}, Valor: {n.nota}, ")
        
    evaluacion = session.query(Evaluacion).filter(Evaluacion.id == 1).first()
    print("Notas del evalauciones pito chico:")
    for n in evaluacion.notas:
        print(f"Evaluación tiene nota {n.id}, valor {n.nota}")

    session.close()
