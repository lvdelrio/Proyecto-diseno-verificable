from sqlalchemy.orm import Session
from db.models.evaluacion import Evaluacion
from db.controller.common_controller import (get_evaluaciones_by_categoria_id,
                                              get_categorias_by_seccion_id)


def prorate_values(valores: list[float]):
    suma_actual = sum(valores)
    if suma_actual == 0:
        return valores
    return [(valor / suma_actual) * 100 for valor in valores]

def recalculate_categoria_ponderations(db: Session, categoria_id: int):
    evaluaciones = get_evaluaciones_by_categoria_id(db, categoria_id)
    if not evaluaciones:
        return
    total_ponderacion = sum(e.ponderacion for e in evaluaciones)
    excess_ponderacion = abs(total_ponderacion - 100.0)

    if excess_ponderacion < 0.01:
        return
    nuevos_valores = prorate_values([e.ponderacion for e in evaluaciones])
    for evaluacion, nuevo_valor in zip(evaluaciones, nuevos_valores):
        evaluacion.ponderacion = round(nuevo_valor, 2)

    db.commit()

def recalculate_seccion_ponderations(db: Session, seccion_id: int):
    categorias = get_categorias_by_seccion_id(db, seccion_id)
    if not categorias:
        return
    total_ponderacion = sum(e.ponderacion for e in categorias)
    excess_ponderacion = abs(total_ponderacion - 100.0)

    if excess_ponderacion < 0.01:
        return
    nuevos_valores = prorate_values([e.ponderacion for e in categorias])
    for categoria, nuevo_valor in zip(categorias, nuevos_valores):
        categoria.ponderacion = round(nuevo_valor, 2)

    db.commit()
