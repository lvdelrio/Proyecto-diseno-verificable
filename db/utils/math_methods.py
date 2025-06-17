from sqlalchemy.orm import Session
from collections import defaultdict
from db.controller.common_controller import get_categorias_by_seccion_id
NOTA_MINIMA = 1

def percentage_sum_from_seccion_by_id(session: Session, seccion_id: int):
    categorias = get_categorias_by_seccion_id(session, seccion_id)
    percentage_sum = sum(categoria.ponderacion for categoria in categorias)
    return percentage_sum

def calculate_average_from_notas(notas, curso_id):
    if not notas:
        return NOTA_MINIMA

    notas_curso = [
        nota for nota in notas
        if nota.evaluacion and
           nota.evaluacion.categoria and
           nota.evaluacion.categoria.seccion and
           nota.evaluacion.categoria.seccion.curso_id == curso_id
    ]

    if not notas_curso:
        return NOTA_MINIMA

    categorias = defaultdict(list)

    for nota in notas_curso:
        categoria = nota.evaluacion.categoria
        categorias[categoria].append(nota)

    total = 0.0
    total_categoria_ponderacion = 0.0

    for categoria, notas_de_categoria in categorias.items():
        ponderacion_categoria = categoria.ponderacion
        total_categoria_ponderacion += ponderacion_categoria

        sum_eval = sum(n.nota * n.evaluacion.ponderacion for n in notas_de_categoria)
        sum_ponderacion = sum(n.evaluacion.ponderacion for n in notas_de_categoria)

        if sum_ponderacion == 0:
            continue

        promedio_categoria = sum_eval / sum_ponderacion
        total += promedio_categoria * ponderacion_categoria

    return total / total_categoria_ponderacion if total_categoria_ponderacion else NOTA_MINIMA
