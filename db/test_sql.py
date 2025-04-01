
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

    nota = Notas(nota=6.5, alumno=alumno, evaluacion=evaluacion)

    session.add(nota)
    session.commit()

    print(f"Nota creada: {nota.id}, valor: {nota.nota}")
    alumno_con_notas = session.query(Alumno).filter(Alumno.id == 1).first()
    print("Notas del Alumno:")
    for n in alumno_con_notas.notas:
        print(f" - Nota ID: {n.id}, Valor: {n.nota}, ")
        
    evaluacion = session.query(Evaluacion).filter(Evaluacion.id == 1).first()
    print("Notas del evalauciones:")
    for n in evaluacion.notas:
        print(f"Evaluación tiene nota {n.id}, valor {n.nota}")

    #secciones test para ver si funcionan las relaciones con evalauciones
    #y sus parametros y las notas
    from db.models.secciones import Seccion
    seccion = session.query(Seccion).filter(Seccion.id == 1).first()
    #sino encuentra crear uno
    if not seccion:
        seccion = Seccion(id=1, nombre="Seccion 1", evaluacion=[evaluacion])
        session.add(seccion)
        session.commit()
    print(f"Seccion: {seccion.id}, Nombre: {seccion.nombre}, Evaluaciones: {seccion.evaluacion}")

    for e in seccion.evaluacion:
        print(f"Evaluacion: {e.id}, Tipo: {e.tipo}, Ponderacion: {e.ponderacion}, Opcional: {e.opcional}")

    for n in seccion.evaluacion[0].notas:
        print(f"Nota: {n.id}, Valor: {n.nota}")

    #testear cursos y sus cursos requisitos
    from db.models.requisitos import CursoRequisito
    from db.models.curso import Curso
    
    curso = Curso(nombre="Física II", descripcion="Curso de Física II")
    requisito = Curso(nombre="Física I", descripcion="Curso de Física I")
    db.session.add_all([curso, requisito])
    db.session.commit()

    curso_requisito = CursoRequisito(curso_id=curso.id, curso_requisito_id=requisito.id)
    db.session.add(curso_requisito)
    db.session.commit()

    print(f"Curso: {curso.nombre}, Requisitos: {[r.curso_requisito.nombre for r in curso.requisitos]}")
    #print(f"Requisito: {requisito.nombre}, Cursos: {[c.curso.nombre for c in requisito.cursos]}")

    session.close()
