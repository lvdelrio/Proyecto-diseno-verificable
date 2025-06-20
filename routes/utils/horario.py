import os
from datetime import datetime
import pandas as pd

DAYS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
MORNING_HOUR_START = 9
MORNING_HOUR_FINISH = 13
AFTERNOON_HOUR_START = 14
AFTERNOON_HOUR_FINISH = 18

SPACER = "  |   "

MORNING_BLOCKS = list(range(MORNING_HOUR_START, MORNING_HOUR_FINISH))
AFTERNOON_BLOCKS = list(range(AFTERNOON_HOUR_START, AFTERNOON_HOUR_FINISH))
AVAILABLE_BLOCKS = [(day, hour) for day in DAYS for hour in MORNING_BLOCKS + AFTERNOON_BLOCKS]
EXPORT_FOLDER = "exports"


def is_valid_block(hour_start: int, duration: int):
    if hour_start + duration > AFTERNOON_HOUR_FINISH:
        return False
    if hour_start < MORNING_HOUR_FINISH < hour_start + duration:
        return False
    return True

def is_block_conflicted(seccion,
                        day,
                        start_hour,
                        sala_id,
                        duration,
                        room_occupancy,
                        teacher_occupancy,
                        student_occupancy):
    for hour in range(start_hour, start_hour + duration):
        if hour == MORNING_HOUR_FINISH:
            return True
        block = (day, hour)

        if block in room_occupancy.get(sala_id, set()):
            return True
        for teacher in seccion.profesores:
            if block in teacher_occupancy.get(teacher.id, set()):
                return True
        for student in seccion.alumnos:
            if block in student_occupancy.get(student.id, set()):
                return True
    return False

def room_fits_section(seccion, room):
    return len(seccion.alumnos) <= room.capacidad

def get_available_start_times(credit_hours):
    return [(day, hour) for (day, hour) in AVAILABLE_BLOCKS if is_valid_block(hour, credit_hours)]

def try_assign_block(seccion, day, hour, room, credit_hours,
                     room_occupancy, teacher_occupancy, student_occupancy,
                     horario_dict):
    if is_block_conflicted(seccion, day, hour, room.id, credit_hours,
                           room_occupancy, teacher_occupancy, student_occupancy):
        return False

    for h in range(hour, hour + credit_hours):
        block = (day, h)
        room_occupancy.setdefault(room.id, set()).add(block)
        for teacher in seccion.profesores:
            teacher_occupancy.setdefault(teacher.id, set()).add(block)
        for student in seccion.alumnos:
            student_occupancy.setdefault(student.id, set()).add(block)

    sec_id = str(seccion.id)
    horario_entry = horario_dict.setdefault(sec_id, {})
    horario_entry.update({
        "Sección": seccion.nombre,
        "Curso": seccion.curso.tipo_curso.descripcion,
        "Créditos": credit_hours,
        "Profesor(es)": ", ".join(p.nombre for p in seccion.profesores),
        "Sala": room.nombre,
        day: f"{hour:02}:00-{hour + credit_hours:02}:00"
    })
    return True

def assign_section_to_horario(seccion,
                              credit_hours,
                              rooms,
                              room_occupancy,
                              teacher_occupancy,
                              student_occupancy,
                              horario_dict):
    for room in rooms:
        if not room_fits_section(seccion, room):
            continue
        for day, hour in get_available_start_times(credit_hours):
            if try_assign_block(seccion, day, hour, room, credit_hours,
                                room_occupancy, teacher_occupancy,
                                student_occupancy, horario_dict):
                return True
    return False

def export_horario_to_csv(horario_dict):
    os.makedirs(EXPORT_FOLDER, exist_ok=True)
    filename = f"horario_tabular_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = os.path.join(EXPORT_FOLDER, filename)

    df = pd.DataFrame(horario_dict.values())
    df.to_csv(filepath, index=False)
    return filepath

def print_excluded_seccion_header():
    print("Seccion excluidas del horario:")
    print("SECCION ID   |   CODIGO CURSO    |   DESCRIPCION CURSO   |   CREDITOS")

def row_display_format(seccion_id, codigo, descripcion, creditos):
    print(SPACER, seccion_id, SPACER, codigo, SPACER, descripcion, SPACER, creditos)
