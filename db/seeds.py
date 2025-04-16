from datetime import datetime

from db.config import db as config
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
from db.models.tipo_curso import TipoCurso
from db.controller.profesor_controller import create_profesor, enroll_profesor_in_seccion
from db.controller.notas_finales_controller import create_nota_final
from db.controller.curso_controller import create_curso
from db.controller.alumno_controller import create_alumno, enroll_alumno_in_seccion
from db.controller.categoria_controller import create_categoria
from db.controller.evaluacion_controller import create_evaluacion
from db.controller.seccion_controller import create_seccion
from db.controller.tipo_curso_controller import create_tipo_curso, enroll_tipo_curso_in_tipo_cursos


def seed_database():
    tipo_curso_1 = create_tipo_curso(config.session, name="Calculo 1", description="Matematicas")
    tipo_curso_2 = create_tipo_curso(config.session, name="Calculo 2", description="Matematicas")
    tipo_curso_3 = create_tipo_curso(config.session, name="Calculo 3", description="Matematicas")
    tipo_curso_4 = create_tipo_curso(config.session, name="Economia", description="Economica")
    tipo_curso_5 = create_tipo_curso(config.session, name="Fisica 1", description="Fisica")
    tipo_curso_6 = create_tipo_curso(config.session, name="Electricidad", description="Fisica")

    requisito1 = enroll_tipo_curso_in_tipo_cursos(config.session, tipo_curso_base_id=tipo_curso_2.id, tipo_curso_id=tipo_curso_1.id)
    requisito1 = enroll_tipo_curso_in_tipo_cursos(config.session, tipo_curso_base_id=tipo_curso_3.id, tipo_curso_id=tipo_curso_2.id)
    requisito1 = enroll_tipo_curso_in_tipo_cursos(config.session, tipo_curso_base_id=tipo_curso_4.id, tipo_curso_id=tipo_curso_1.id)
    requisito1 = enroll_tipo_curso_in_tipo_cursos(config.session, tipo_curso_base_id=tipo_curso_5.id, tipo_curso_id=tipo_curso_2.id)
    requisito1 = enroll_tipo_curso_in_tipo_cursos(config.session, tipo_curso_base_id=tipo_curso_6.id, tipo_curso_id=tipo_curso_3.id)
    requisito1 = enroll_tipo_curso_in_tipo_cursos(config.session, tipo_curso_base_id=tipo_curso_6.id, tipo_curso_id=tipo_curso_5.id)

    curso1 = create_curso(config.session, tipo_curso_id=tipo_curso_1.id, fecha_impartida=2020, semestre_impartido="Anual")
    curso2 = create_curso(config.session, tipo_curso_id=tipo_curso_1.id, fecha_impartida=2021, semestre_impartido="Anual")
    curso3 = create_curso(config.session, tipo_curso_id=tipo_curso_2.id, fecha_impartida=2020, semestre_impartido="Primer Semestre")
    curso4 = create_curso(config.session, tipo_curso_id=tipo_curso_2.id, fecha_impartida=2020, semestre_impartido="Segundo Semestre")
    curso5 = create_curso(config.session, tipo_curso_id=tipo_curso_3.id, fecha_impartida=2020, semestre_impartido="Anual")
    curso6 = create_curso(config.session, tipo_curso_id=tipo_curso_4.id, fecha_impartida=2020, semestre_impartido="Primer Semestre")
    curso7 = create_curso(config.session, tipo_curso_id=tipo_curso_5.id, fecha_impartida=2020, semestre_impartido="Anual")
    curso8 = create_curso(config.session, tipo_curso_id=tipo_curso_6.id, fecha_impartida=2021, semestre_impartido="Primer Semestre")
    curso9 = create_curso(config.session, tipo_curso_id=tipo_curso_6.id, fecha_impartida=2022, semestre_impartido="Primer Semestre")

    seccion1 = create_seccion(config.session, curso_id=curso1.id, nombre="seccion 1")
    seccion2 = create_seccion(config.session, curso_id=curso1.id, nombre="seccion 2")
    seccion3 = create_seccion(config.session, curso_id=curso1.id, nombre="seccion 3")
    seccion4 = create_seccion(config.session, curso_id=curso1.id, nombre="seccion 4")
    seccion5 = create_seccion(config.session, curso_id=curso2.id, nombre="seccion 1")
    seccion6 = create_seccion(config.session, curso_id=curso3.id, nombre="seccion 1")
    seccion7 = create_seccion(config.session, curso_id=curso4.id, nombre="seccion 1")
    seccion8 = create_seccion(config.session, curso_id=curso4.id, nombre="seccion 2")
    seccion9 = create_seccion(config.session, curso_id=curso5.id, nombre="seccion 1")
    seccion10 = create_seccion(config.session, curso_id=curso5.id, nombre="seccion 2")
    seccion11 = create_seccion(config.session, curso_id=curso5.id, nombre="seccion 3")
    seccion12 = create_seccion(config.session, curso_id=curso5.id, nombre="seccion 4")
    seccion13 = create_seccion(config.session, curso_id=curso5.id, nombre="seccion 5")
    seccion14 = create_seccion(config.session, curso_id=curso5.id, nombre="seccion 6")
    seccion15 = create_seccion(config.session, curso_id=curso5.id, nombre="seccion 7")
    seccion16 = create_seccion(config.session, curso_id=curso6.id, nombre="seccion 1")
    seccion17 = create_seccion(config.session, curso_id=curso7.id, nombre="seccion 1")
    seccion18 = create_seccion(config.session, curso_id=curso8.id, nombre="seccion 1")
    seccion19 = create_seccion(config.session, curso_id=curso9.id, nombre="seccion 1")
    seccion20 = create_seccion(config.session, curso_id=curso9.id, nombre="seccion 2")

    alumno1 = create_alumno(config.session, name="Lucas", email="Lucas@gmail.cl", fecha_ingreso="2025-04-07")
    alumno2 = create_alumno(config.session, name="Paulo", email="Paulo@gmail.cl", fecha_ingreso="2025-04-07")
    alumno3 = create_alumno(config.session, name="Raul", email="Raul@gmail.cl", fecha_ingreso="2025-04-07")
    alumno4 = create_alumno(config.session, name="Carlos", email="Carlos@gmail.cl", fecha_ingreso="2025-04-07")
    alumno5 = create_alumno(config.session, name="Sergio", email="Sergio@gmail.cl", fecha_ingreso="2025-04-07")
    alumno6 = create_alumno(config.session, name="Sebastian", email="Sebastian@gmail.cl", fecha_ingreso="2025-04-07")
    alumno7 = create_alumno(config.session, name="Esteban", email="Esteban@gmail.cl", fecha_ingreso="2025-04-07")
    alumno8 = create_alumno(config.session, name="Santiago", email="Santiago@gmail.cl", fecha_ingreso="2025-04-07")
    alumno9 = create_alumno(config.session, name="Fernando", email="Fernando@gmail.cl", fecha_ingreso="2025-04-07")
    alumno10 = create_alumno(config.session, name="Francisco", email="Francisco@gmail.cl", fecha_ingreso="2025-04-07")
    alumno11 = create_alumno(config.session, name="Pedro", email="Pedro@gmail.cl", fecha_ingreso="2025-04-07")
    alumno12 = create_alumno(config.session, name="Cristobal", email="Cristobal@gmail.cl", fecha_ingreso="2025-04-07")
    alumno13 = create_alumno(config.session, name="Nicolas", email="Nicolas@gmail.cl", fecha_ingreso="2025-04-07")
    alumno14 = create_alumno(config.session, name="Marcelo", email="Marcelo@gmail.cl", fecha_ingreso="2025-04-07")
    alumno15 = create_alumno(config.session, name="Jorge", email="Jorge@gmail.cl", fecha_ingreso="2025-04-07")
    alumno16 = create_alumno(config.session, name="Domingo", email="Domingo@gmail.cl", fecha_ingreso="2025-04-07")

    alumno_seccion_1 = enroll_alumno_in_seccion(config.session, alumno_id=alumno1.id, seccion_id=seccion6.id)
    alumno_seccion_2 = enroll_alumno_in_seccion(config.session, alumno_id=alumno2.id, seccion_id=seccion1.id)
    alumno_seccion_3 = enroll_alumno_in_seccion(config.session, alumno_id=alumno3.id, seccion_id=seccion1.id)
    alumno_seccion_4 = enroll_alumno_in_seccion(config.session, alumno_id=alumno4.id, seccion_id=seccion1.id)
    alumno_seccion_5 = enroll_alumno_in_seccion(config.session, alumno_id=alumno5.id, seccion_id=seccion1.id)
    alumno_seccion_6 = enroll_alumno_in_seccion(config.session, alumno_id=alumno6.id, seccion_id=seccion1.id)
    alumno_seccion_7 = enroll_alumno_in_seccion(config.session, alumno_id=alumno7.id, seccion_id=seccion1.id)
    alumno_seccion_8 = enroll_alumno_in_seccion(config.session, alumno_id=alumno8.id, seccion_id=seccion1.id)
    alumno_seccion_9 = enroll_alumno_in_seccion(config.session, alumno_id=alumno9.id, seccion_id=seccion1.id)
    alumno_seccion_10 = enroll_alumno_in_seccion(config.session, alumno_id=alumno10.id, seccion_id=seccion1.id)
    alumno_seccion_11 = enroll_alumno_in_seccion(config.session, alumno_id=alumno10.id, seccion_id=seccion16.id)

    profesor1 = create_profesor(config.session, nombre="Raul", email="Raul@gmail.com")
    profesor2 = create_profesor(config.session, nombre="Miguel", email="Miguel@gmail.com")
    profesor3 = create_profesor(config.session, nombre="San Miguel", email="San Miguel@gmail.com")
    profesor4 = create_profesor(config.session, nombre="Jose", email="Jose@gmail.com")
    profesor5 = create_profesor(config.session, nombre="Carlos", email="Carlos@gmail.com")
    profesor6 = create_profesor(config.session, nombre="Unicua", email="Unicua@gmail.com")

    profesor_seccion_1 = enroll_profesor_in_seccion(config.session, profesor_id=profesor1.id, seccion_id=seccion1.id)
    profesor_seccion_2 = enroll_profesor_in_seccion(config.session, profesor_id=profesor2.id, seccion_id=seccion1.id)
    profesor_seccion_3 = enroll_profesor_in_seccion(config.session, profesor_id=profesor3.id, seccion_id=seccion1.id)
    profesor_seccion_4 = enroll_profesor_in_seccion(config.session, profesor_id=profesor1.id, seccion_id=seccion16.id)
    profesor_seccion_5 = enroll_profesor_in_seccion(config.session, profesor_id=profesor1.id, seccion_id=seccion17.id)
    profesor_seccion_6 = enroll_profesor_in_seccion(config.session, profesor_id=profesor2.id, seccion_id=seccion5.id)
    profesor_seccion_7 = enroll_profesor_in_seccion(config.session, profesor_id=profesor3.id, seccion_id=seccion10.id)

