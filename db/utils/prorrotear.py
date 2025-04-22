from sqlalchemy.orm import Session
from ..models.evaluacion import Evaluacion
from ..controller.common_controller import get_evaluaciones_by_categoria


def prorate_values(valores: list[float]):
    suma_actual = sum(valores)
    if suma_actual == 0:
        return valores  
    return [(valor / suma_actual) * 100 for valor in valores]

def recalculate_categoria_ponderations(db: Session, categoria_id: int):
    evaluaciones = get_evaluaciones_by_categoria(db, categoria_id)
    if not evaluaciones:
        return 
    total_ponderacion = sum(e.ponderacion for e in evaluaciones)

    if abs(total_ponderacion - 100.0) < 0.01:
        return 
    nuevos_valores = prorate_values([e.ponderacion for e in evaluaciones])
    for evaluacion, nuevo_valor in zip(evaluaciones, nuevos_valores):
        evaluacion.ponderacion = round(nuevo_valor, 2)

    db.commit()
