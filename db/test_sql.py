
from db.config import db
from db.models.alumno import Alumno
from db.models.notas import Notas
from db.models.evaluacion import Evaluacion
from db.models.categoria import Categoria
from db.models.notas_finales import NotasFinales
from db.models.alumno_seccion import AlumnoSeccion
from db.models.profesor import Profesor
from db.models.curso import Curso
from db.models.requisitos import CursoRequisito
from db.models.seccion import Seccion
#from db.controller.notas_controller import crear_nota
from db.controller.notas_finales_controller import create_nota_final
from db.controller.curso_controller import crear_curso
from db.controller.alumno_controller import create_alumno
from db.controller.categoria_controller import create_categoria
from db.controller.evalaucion_controller import create_evaluacion
from db.controller.seccion_controller import crear_seccion
def test_sql():
    session = db.session

    alumno = session.query(Alumno).filter(Alumno.id == 1).first()
    evaluacion = session.query(Evaluacion).filter(Evaluacion.id == 1).first()
    if not evaluacion:
        evaluacion = create_evaluacion( tipo=1, ponderacion=0.5, opcional=1)
        session.commit()
    if not alumno:
        alumno = create_alumno(session, name="test", email="test", fecha_ingreso="2023-01-01")


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

    #secciones test para ver si funcionan las relaciones con categorias
    #y sus parametros y las notas
    from db.models.seccion import Seccion
    seccion = session.query(Seccion).filter(Seccion.id == 1).first()
    #sino encuentra crear uno
    if not seccion:
        seccion = Seccion(id=1, nombre="Seccion 1")
        session.add(seccion)
        session.commit()
    
    categoria = create_categoria(
    tipo_categoria="Pruebas",
    seccion = seccion,
    ponderacion=0.5,
    opcional=False
    )

    print(f"Seccion: {seccion.id}, Nombre: {seccion.nombre}, Evaluaciones: {seccion.categorias}")

    #testear cursos y sus cursos requisitos
    
    curso = Curso(nombre="Física II", descripcion="Curso de Física II", semestre_de_ejecucion=1)
    requisito = Curso(nombre="Física I", descripcion="Curso de Física I", semestre_de_ejecucion=2)
    db.session.add_all([curso, requisito])
    db.session.commit()

    curso_requisito = CursoRequisito(curso_id=curso.id, curso_requisito_id=requisito.id)
    db.session.add(curso_requisito)
    db.session.commit()

    print(f"Curso: {curso.nombre}, Requisitos: {[r.curso_requisito.nombre for r in curso.requisitos]}")
    #print(f"Requisito: {requisito.nombre}, Cursos: {[c.curso.nombre for c in requisito.cursos]}")
    #alumno con notas finales y cursos

    curso = session.query(Curso).filter(Curso.id == 1).first()
    if not curso:
        curso = crear_curso(session, "Curso de prueba", "Descripcion del curso")
        session.commit()
    print(f"Curso: {curso.id}, Nombre: {curso.nombre}, Descripcion: {curso.descripcion}")

    notas_finales = session.query(NotasFinales).filter(NotasFinales.id == 1).first()
    if not notas_finales:
        notas_finales = NotasFinales(nota_final=4.5, alumno=alumno, curso=curso)
        session.add(notas_finales)
        session.commit()
    
    print(f"Nota final: {notas_finales.id}, Valor: {notas_finales.nota_final}")
    print(f"Alumno: {notas_finales.alumno.nombre}, Curso: {notas_finales.curso.nombre}")
    #mostrar todas las notas finales de los distintos cursos de un solo alumno

    print("Notas finales del alumno:")
    for n in alumno.notas_finales:
        print(f" - Nota ID: {n.id}, Valor: {n.nota_final}, Curso: {n.curso.nombre}")
    print(f"Notas finales del alumno: {alumno.notas_finales}")
    # Verificar si la relación entre alumno y notas finales funciona

    #crear categoria y evalaucio y llamar ambas desde ambas

    
    # Verificando relaciones
    print("Categoría creada:", categoria)
    print("Evaluaciones asociadas a esta categoría:")
    for evaluacion in categoria.evaluaciones:
        print(f"- Evaluacion ID: {evaluacion.id}, Tipo: {evaluacion.tipo}, Opcional: {evaluacion.opcional}")

    #ver alumno con sus secciones y secciones con sus alumnos usando la tabla intermedia alumno-secciones

    alumno = session.query(Alumno).filter(Alumno.id == 1).first()
    if not alumno:
        alumno = Alumno(id=1, nombre="Lucas", email="lucas@example.com", fecha_ingreso="2024-04-14")
        session.add(alumno)
        session.commit()

    secciones = alumno.secciones
    if not secciones:
        seccion = session.query(Seccion).filter(Seccion.id == 1).first()
        if not seccion:
            seccion = Seccion(id=1, nombre="Sección 1")
            session.add(seccion)
            session.commit()
        alumno_seccion = AlumnoSeccion(alumno_id=alumno.id, seccion_id=seccion.id)
        session.add(alumno_seccion)
        session.commit()
        session.refresh(alumno)
        secciones = alumno.secciones

    print(f"Alumno: {alumno.id}, Nombre: {alumno.nombre}, Secciones: {[s.id for s in secciones]}")

    seccion = session.query(Seccion).filter(Seccion.id == 1).first()
    alumnos = seccion.alumnos
    print(f"Seccion: {seccion.id}, Nombre: {seccion.nombre}, Alumnos: {[a.id for a in alumnos]}")

    session.close()
