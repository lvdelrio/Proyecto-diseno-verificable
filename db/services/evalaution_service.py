from ..utils.extract_number import extract_number_from_name

INDEX = 1

def get_evaluacion_by_instancia(evaluaciones, instancia):
    evaluaciones_sorted = sorted(evaluaciones, key=extract_number_from_name)
    return evaluaciones_sorted[instancia - INDEX]