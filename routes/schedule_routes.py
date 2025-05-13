from flask import Blueprint, jsonify
from collections import defaultdict
from db.config import db as config
from db.controller.tipo_curso_controller import get_all_tipo_cursos
from db.controller.curso_controller import get_all_cursos
from db.controller.seccion_controller import get_all_secciones
from db.controller.profesor_controller import get_all_profesores
from db.controller.alumno_controller import get_all_alumnos
from db.controller.sala_controller import get_all_salas
from routes.utils.horario import assign_section_to_schedule, export_schedule_to_csv


schedule_route_blueprint = Blueprint("Schedule", __name__)

@schedule_route_blueprint.route('/crear_horario', methods=['GET', 'POST'])
def create_horario():
    secciones = get_all_secciones(config.session)
    salas = get_all_salas(config.session)

    room_occupancy = {}
    teacher_occupancy = {}
    student_occupancy = {}

    schedule_by_section = defaultdict(lambda: {
        "Sección": "",
        "Curso": "",
        "Créditos": 0,
        "Profesor(es)": "",
        "Sala": "",
        "Lunes": "",
        "Martes": "",
        "Miércoles": "",
        "Jueves": "",
        "Viernes": ""
    })

    for seccion in secciones:
        if not seccion.curso or not seccion.curso.tipo_curso:
            continue
        credit_hours = seccion.curso.tipo_curso.creditos
        success = assign_section_to_schedule(
            seccion, credit_hours, salas,
            room_occupancy, teacher_occupancy,
            student_occupancy, schedule_by_section
        )
        if not success:
            print(f"[!] No se pudo asignar sección {seccion.nombre} (ID {seccion.id})")

    filepath = export_schedule_to_csv(schedule_by_section)
    return jsonify({"status": "ok", "mensaje": "Horario generado", "archivo": filepath})
