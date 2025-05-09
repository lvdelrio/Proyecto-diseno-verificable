from db.models.seccion import Seccion
from db.controller.curso_controller import get_all_cursos
from db.controller.sala_controller import get_all_salas
from db.controller.seccion_controller import get_all_secciones
from db.controller.profesor_controller import get_all_profesores
from db.controller.alumno_controller import get_all_alumnos
import pandas as pd

HORAS_DISPONIBLES = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
DIAS = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']

# Validación para evitar asignar horario de colación
def es_hora_colacion(hora):
    return hora == 13

# Función principal para asignar horarios
def assignacion_horario():
    salas = get_all_salas()
    secciones = get_all_secciones()

    asignaciones = []

    horario_usado = {
        'salas': {},
        'profesores': {},
        'alumnos': {},
    }

    for seccion in secciones:
        curso = seccion.curso
        creditos = curso.tipo_curso.creditos

        asignado = False

        for dia in DIAS:
            for hora_inicio in HORAS_DISPONIBLES:
                if es_hora_colacion(hora_inicio) or es_hora_colacion(hora_inicio + creditos - 1):
                    continue

                if hora_inicio + creditos - 1 > max(HORAS_DISPONIBLES):
                    continue

                horario_conflicto = False

                for hora in range(hora_inicio, hora_inicio + creditos):
                    clave_horario = f"{dia}_{hora}"

                    sala_ocupada = horario_usado['salas'].get(seccion.sala.id, {}).get(clave_horario, False)
                    profesor_ocupado = any(horario_usado['profesores'].get(prof.id, {}).get(clave_horario, False) for prof in seccion.profesores)
                    alumno_ocupado = any(horario_usado['alumnos'].get(alum.id, {}).get(clave_horario, False) for alum in seccion.alumnos)

                    if sala_ocupada or profesor_ocupado or alumno_ocupado:
                        horario_conflicto = True
                        break

                if not horario_conflicto:
                    for hora in range(hora_inicio, hora_inicio + creditos):
                        clave_horario = f"{dia}_{hora}"
                        horario_usado['salas'].setdefault(seccion.sala.id, {})[clave_horario] = True

                        for prof in seccion.profesores:
                            horario_usado['profesores'].setdefault(prof.id, {})[clave_horario] = True

                        for alum in seccion.alumnos:
                            horario_usado['alumnos'].setdefault(alum.id, {})[clave_horario] = True

                    asignaciones.append({
                        'Curso': curso.nombre,
                        'Seccion': seccion.nombre,
                        'Sala': seccion.sala.nombre,
                        'Profesor(es)': ", ".join([prof.nombre for prof in seccion.profesores]),
                        'Alumnos': ", ".join([alum.nombre for alum in seccion.alumnos]),
                        'Dia': dia,
                        'Hora Inicio': f"{hora_inicio}:00",
                        'Hora Fin': f"{hora_inicio + creditos}:00"
                    })
                    asignado = True
                    break

            if asignado:
                break

        if not asignado:
            print(f"No se pudo asignar horario para sección {seccion.nombre} del curso {curso.nombre}")

    exportar_excel(asignaciones)

# Función para exportar asignaciones a Excel
def exportar_excel(asignaciones):
    df = pd.DataFrame(asignaciones)
    df.to_excel('asignacion_horarios.xlsx', index=False)
    print("Horarios asignados exportados a Excel exitosamente.")

if __name__ == '__main__':
    assignacion_horario()