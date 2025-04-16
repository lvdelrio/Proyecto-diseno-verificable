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
from db.models.tipo_curso import TipoCurso
#from db.controller.notas_controller import crear_nota
from db.controller.notas_finales_controller import create_nota_final
from db.controller.curso_controller import create_curso
from db.controller.alumno_controller import create_alumno
from db.controller.categoria_controller import create_categoria
from db.controller.evaluacion_controller import create_evaluacion
from db.controller.seccion_controller import create_seccion
from db.controller.tipo_curso_controller import create_tipo_curso, enroll_tipo_curso_in_tipo_cursos



tipo_curso_1 = create_tipo_curso(name="Calculo 1", description="Matematicas")
tipo_curso_2 = create_tipo_curso(name="Calculo 2", description="Matematicas")
tipo_curso_3 = create_tipo_curso(name="Calculo 3", description="Matematicas")
tipo_curso_4 = create_tipo_curso(name="Economia", description="Economica")
tipo_curso_5 = create_tipo_curso(name="Fisica 1", description="Fisica")
tipo_curso_6 = create_tipo_curso(name="Electricidad y magnetismo", description="Fisica")

requisito1 = enroll_tipo_curso_in_tipo_cursos(tipo_curso_base_id=tipo_curso_2.id, tipo_curso_id=tipo_curso_1.id)
requisito1 = enroll_tipo_curso_in_tipo_cursos(tipo_curso_base_id=tipo_curso_3.id, tipo_curso_id=tipo_curso_2.id)
requisito1 = enroll_tipo_curso_in_tipo_cursos(tipo_curso_base_id=tipo_curso_4.id, tipo_curso_id=tipo_curso_1.id)
requisito1 = enroll_tipo_curso_in_tipo_cursos(tipo_curso_base_id=tipo_curso_5.id, tipo_curso_id=tipo_curso_2.id)
requisito1 = enroll_tipo_curso_in_tipo_cursos(tipo_curso_base_id=tipo_curso_6.id, tipo_curso_id=tipo_curso_3.id)
requisito1 = enroll_tipo_curso_in_tipo_cursos(tipo_curso_base_id=tipo_curso_6.id, tipo_curso_id=tipo_curso_5.id)

curso1 = create_curso(tipo_curso_id=tipo_curso_1.id, fecha_impartida=2020, imparted_semester="Anual")
curso2 = create_curso(tipo_curso_id=tipo_curso_1.id, fecha_impartida=2021, imparted_semester="Anual")
curso3 = create_curso(tipo_curso_id=tipo_curso_2.id, fecha_impartida=2020, imparted_semester="Primer Semestre")
curso4 = create_curso(tipo_curso_id=tipo_curso_2.id, fecha_impartida=2020, imparted_semester="Segundo Semestre")
curso5 = create_curso(tipo_curso_id=tipo_curso_3.id, fecha_impartida=2020, imparted_semester="Anual")
curso6 = create_curso(tipo_curso_id=tipo_curso_4.id, fecha_impartida=2020, imparted_semester="Primer Semestre")
curso7 = create_curso(tipo_curso_id=tipo_curso_5.id, fecha_impartida=2020, imparted_semester="Anual")
curso8 = create_curso(tipo_curso_id=tipo_curso_6.id, fecha_impartida=2021, imparted_semester="Primer Semestre")
curso9 = create_curso(tipo_curso_id=tipo_curso_6.id, fecha_impartida=2022, imparted_semester="Primer Semestre")



seccion1 = create_seccion(curso_id=curso1.id, nombre="seccion 1")
seccion2 = create_seccion(curso_id=curso1.id, nombre="seccion 2")
seccion3 = create_seccion(curso_id=curso1.id, nombre="seccion 3")
seccion4 = create_seccion(curso_id=curso1.id, nombre="seccion 4")
seccion5 = create_seccion(curso_id=curso2.id, nombre="seccion 1")
seccion6 = create_seccion(curso_id=curso3.id, nombre="seccion 1")
seccion7 = create_seccion(curso_id=curso4.id, nombre="seccion 1")
seccion8 = create_seccion(curso_id=curso4.id, nombre="seccion 2")
seccion9 = create_seccion(curso_id=curso5.id, nombre="seccion 1")
seccion10 = create_seccion(curso_id=curso5.id, nombre="seccion 2")
seccion11 = create_seccion(curso_id=curso5.id, nombre="seccion 3")
seccion12 = create_seccion(curso_id=curso5.id, nombre="seccion 4")
seccion13 = create_seccion(curso_id=curso5.id, nombre="seccion 5")
seccion14 = create_seccion(curso_id=curso5.id, nombre="seccion 6")
seccion15 = create_seccion(curso_id=curso5.id, nombre="seccion 7")
seccion16 = create_seccion(curso_id=curso6.id, nombre="seccion 1")
seccion17 = create_seccion(curso_id=curso7.id, nombre="seccion 1")
seccion18 = create_seccion(curso_id=curso8.id, nombre="seccion 1")
seccion19 = create_seccion(curso_id=curso9.id, nombre="seccion 1")
seccion20 = create_seccion(curso_id=curso9.id, nombre="seccion 2")

# alumno1 = create_alumno(name="Lucas", email="Lucas@gmail.cl", fecha_de_ingreso=)
# alumno2 = create_alumno(name="Paulo", email="Paulo@gmail.cl", fecha_de_ingreso=)
# alumno3 = create_alumno(name="Raul", email="Raul@gmail.cl", fecha_de_ingreso=)
# alumno4 = create_alumno(name="Carlos", email="Carlos@gmail.cl", fecha_de_ingreso=)
# alumno5 = create_alumno(name="Sergio", email="Sergio@gmail.cl", fecha_de_ingreso=)
# alumno6 = create_alumno(name="Sebastian", email="Sebastian@gmail.cl", fecha_de_ingreso=)
# alumno7 = create_alumno(name="Esteban", email="Estaban@gmail.cl", fecha_de_ingreso=)
# alumno8 = create_alumno(name="Santiago", email="Santiago", fecha_de_ingreso=)
# alumno9 = create_alumno(name="Fernando", email="Fernando@gmail.cl", fecha_de_ingreso=)
# alumno10 = create_alumno(name="Francisco", email="Francisco@gmail.cl", fecha_de_ingreso=)
# alumno11 = create_alumno(name="Pedro", email="Pedro@gmail.cl", fecha_de_ingreso=)
# alumno12 = create_alumno(name="Cristobal", email="Cristobal@gmail.cl", fecha_de_ingreso=)
# alumno13 = create_alumno(name="Nicolas", email="Nicolas@gmail.cl", fecha_de_ingreso=)
# alumno14 = create_alumno(name="Marcelo", email="Marcelo@gmail.cl", fecha_de_ingreso=)
# alumno15 = create_alumno(name="Jorge", email="Jorge@gmail.cl", fecha_de_ingreso=)
# alumno16 = create_alumno(name="Domingo", email="Domingo@gmail.cl", fecha_de_ingreso=)