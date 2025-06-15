INDEX = 1
DEFAULT_NUMBER_OF_EVALUACION = 0

def extract_number_from_name(evaluacion):
    nombre_evaluacion = evaluacion.nombre
    evaluacion_number = nombre_evaluacion.split()[-INDEX]
    if evaluacion_number.isdigit():
        return int(evaluacion_number)
    return DEFAULT_NUMBER_OF_EVALUACION
