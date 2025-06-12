INDEX = 1
def extract_number_from_name(evaluacion):
    nombre_evaluacion = evaluacion.nombre
    evaluacion_number = nombre_evaluacion.split()[-INDEX]
    if evaluacion_number.isdigit():
        return int(evaluacion_number)
    return 0
