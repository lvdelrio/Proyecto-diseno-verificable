from flask import Blueprint, jsonify
from collections import defaultdict
from db.config import db as config
from db.controller.tipo_curso_controller import get_all_tipo_cursos
from db.controller.curso_controller import get_all_cursos
from db.controller.seccion_controller import get_all_secciones
from db.controller.alumno_controller import get_all_alumnos
from db.controller.sala_controller import get_all_salas
from routes.utils.horario import assign_section_to_horario, export_horario_to_csv, print_excluded_seccion_header, row_display_format

CREDITOS_DEFAULT = 0

horario_route_blueprint = Blueprint("Horario", __name__)

@horario_route_blueprint.route('/crear_horario', methods=['GET', 'POST'])
def create_horario():
    secciones = get_all_secciones(config.session)
    salas = get_all_salas(config.session)

    room_occupancy = {}
    teacher_occupancy = {}
    student_occupancy = {}

    horario_by_section = defaultdict(lambda: {
        "Sección": "",
        "Curso": "",
        "Créditos": CREDITOS_DEFAULT,
        "Profesor(es)": "",
        "Sala": "",
        "Lunes": "",
        "Martes": "",
        "Miércoles": "",
        "Jueves": "",
        "Viernes": ""
    })

    print_excluded_seccion_header()
    for seccion in secciones:
        if not seccion.curso or not seccion.curso.tipo_curso:
            continue
        credit_hours = seccion.curso.tipo_curso.creditos
        success = assign_section_to_horario(
            seccion, credit_hours, salas,
            room_occupancy, teacher_occupancy,
            student_occupancy, horario_by_section
        )
        if(not success):
            row_display_format(seccion.id,
                                seccion.curso.tipo_curso.codigo,
                                seccion.curso.tipo_curso.descripcion,
                                seccion.curso.tipo_curso.creditos)

    filepath = export_horario_to_csv(horario_by_section)
    return jsonify({"status": "ok", "mensaje": "Horario generado", "archivo": filepath})
