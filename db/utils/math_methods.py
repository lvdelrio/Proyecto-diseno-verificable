from sqlalchemy.orm import Session
from db.controller.common_controller import get_categorias_by_seccion_id
NOTA_MINIMA = 1

def percentage_sum_from_seccion_by_id(session: Session, seccion_id: int):
    categorias = get_categorias_by_seccion_id(session, seccion_id)
    percentage_sum = sum(categoria.ponderacion for categoria in categorias)
    return percentage_sum

def calculate_average_from_notas(notas):
    if not notas:
        return None
    total = sum(nota.nota * nota.evaluacion.ponderacion for nota in notas)
    total_ponderation = sum(nota.evaluacion.ponderacion for nota in notas)
    return total / total_ponderation if total_ponderation else NOTA_MINIMA
