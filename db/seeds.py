from datetime import datetime
from faker import Faker
from random import sample, choice, randint, uniform

from db.config import db as config
from db.controller.profesor_controller import create_profesor, enroll_profesor_in_seccion
from db.controller.curso_controller import create_curso
from db.controller.alumno_controller import create_alumno, enroll_alumno_in_seccion
from db.controller.seccion_controller import create_seccion, get_all_secciones_by_curso_id
from db.controller.tipo_curso_controller import create_tipo_curso, enroll_tipo_curso_in_tipo_cursos
from db.controller.sala_controller import create_sala
from db.controller.categoria_controller import create_categoria
from db.controller.evaluacion_controller import create_evaluacion
from db.controller.notas_controller import create_nota
from db.controller.common_controller import get_all_alumno__by_categoria_id
from db.utils.prorrotear import prorate_values

def seed_database():
    faker = Faker()

    # Crear salas
    for i in range(1, 6):
        create_sala(config.session, nombre=f"Sala {i}", capacidad=20 + (i % 5) * 5)

    # Crear tipo_cursos
    tipo_cursos = []
    for i in range(15):
        tipo = create_tipo_curso(
            config.session,
            tipo_curso_code=f"TC{i:03}",
            description=faker.bs().capitalize(),
            tipo_curso_credits=randint(1, 4)
        )
        tipo_cursos.append(tipo)

    # Crear requisitos entre tipo_cursos
    for i in range(5, len(tipo_cursos)):
        prereq = choice(tipo_cursos[:i])
        enroll_tipo_curso_in_tipo_cursos(config.session, tipo_curso_base_id=tipo_cursos[i].id, tipo_curso_id=prereq.id)

    # Crear cursos y secciones
    secciones = []
    cursos = []
    for tipo in tipo_cursos:
        for _ in range(2):  # 2 cursos por tipo
            curso = create_curso(
                config.session,
                tipo_curso_id=tipo.id,
                fecha_impartida=randint(2019, 2025),
                semestre_impartido=choice(["Primer Semestre", "Segundo Semestre", "Anual"])
            )
            cursos.append(curso)
            for j in range(2):  # 2 secciones por curso
                seccion = create_seccion(config.session, curso_id=curso.id, nombre=f"Seccion {j+1} - {tipo.codigo}")
                secciones.append(seccion)

    # Crear alumnos
    alumnos = []
    for i in range(150):
        alumno = create_alumno(
            config.session,
            name=faker.first_name(),
            email=f"alumno{i}@ejemplo.com",
            fecha_ingreso="2025-04-07"
        )
        alumnos.append(alumno)

    # Inscribir alumnos en secciones (3 cada uno)
    for alumno in alumnos:
        for curso in sample(cursos, 3):
            seccion = sample(get_all_secciones_by_curso_id(config.session, curso.id), 1)
            enroll_alumno_in_seccion(config.session, alumno_id=alumno.id, seccion_id=seccion[0].id)

    # Crear profesores
    profesores = []
    for i in range(2):
        profesor = create_profesor(
            config.session,
            nombre=faker.name(),
            email=f"profesor{i}@ejemplo.com"
        )
        profesores.append(profesor)

    # Asignar profesores a secciones (cada uno en 3)
    for profesor in profesores:
        for seccion in sample(secciones, 30):
            enroll_profesor_in_seccion(config.session, profesor_id=profesor.id, seccion_id=seccion.id)

    # Crear categorías, evaluaciones y notas vacías por sección
    for seccion in secciones:
        num_categorias = randint(1, 2)
        for i in range(num_categorias):
            tipo_cat = choice(["Controles", "Tareas", "Examen", "Proyecto", "Prácticas"])
            ponderacion_categoria = randint(20, 50)
            tipo_ponderacion = True  # tipo porcentaje

            categoria = create_categoria(
                tipo_categoria=tipo_cat,
                seccion=seccion,
                ponderacion=ponderacion_categoria,
                tipo_ponderacion=tipo_ponderacion
            )

            if not categoria:
                continue

            num_evaluaciones = randint(1, 3)
            pesos = prorate_values([randint(1, 10) for _ in range(num_evaluaciones)])

            for j in range(num_evaluaciones):
                evaluacion = create_evaluacion(
                    db=config.session,
                    nombre=f"{tipo_cat} {j + 1}",
                    ponderacion=pesos[j],
                    opcional=choice([True, False]),
                    categoria_id=categoria.id,
                    tipo_ponderacion=tipo_ponderacion
                )

                if not evaluacion:
                    continue

                # Obtener alumnos en la sección y crear notas vacías
                alumnos_en_seccion = get_all_alumno__by_categoria_id(config.session, categoria.id)
                for alumno in alumnos_en_seccion:
                    create_nota(
                        db=config.session,
                        alumno_id=alumno.id,
                        evaluacion_id=evaluacion.id,
                        nota=round(uniform(3.0, 7.0), 1)
                    )

    print("[+] Base de datos sembrada exitosamente con datos amplios para pruebas de horario.")

