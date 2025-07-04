from flask import abort
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db.config import db
from db.models.categoria import Categoria
from db.models.seccion import Seccion
from db.controller.evaluacion_controller import create_evaluacion
from db.utils.prorrotear import prorate_values
from db.utils.prorrotear import recalculate_seccion_ponderations
from db.utils.math_methods import percentage_sum_from_seccion_by_id
from utils.http_status import BAD_REQUEST, NOT_FOUND

PERCENTAGE_TYPE = 1
MAX_PERCENTAGE = 100

def create_categoria(tipo_categoria, seccion, ponderacion, tipo_ponderacion):
    nueva_categoria = Categoria(
        tipo_categoria=tipo_categoria,
        seccion_id=seccion.id,
        ponderacion=ponderacion,
        tipo_ponderacion=tipo_ponderacion
    )
    if not validation_categoria(nueva_categoria, seccion.id):
        db.session.rollback()
        abort(BAD_REQUEST, description="Error: La categoría no es válida para la sección.")
        return
    db.session.add(nueva_categoria)
    db.session.commit()
    if(percentage_sum_from_seccion_by_id(db.session, nueva_categoria.seccion_id)
        > MAX_PERCENTAGE and nueva_categoria.tipo_ponderacion == PERCENTAGE_TYPE):
        recalculate_seccion_ponderations(db.session, nueva_categoria.seccion_id)
    return nueva_categoria

def get_categoria(categoria_id):
    return Categoria.query.get(categoria_id)

def get_all_categorias_by_seccion_id(seccion_id):
    return Categoria.query.filter_by(seccion_id=seccion_id).all()

def edit_categoria(categoria_id, tipo_categoria=None, seccion_id=None,
                    ponderacion=None, tipo_ponderacion=None):
    categoria = get_categoria(categoria_id)
    if not categoria:
        abort(NOT_FOUND, description="Categoría no encontrada")

    if tipo_categoria is not None:
        categoria.tipo_categoria = tipo_categoria
    if seccion_id is not None:
        categoria.seccion_id = seccion_id
    if ponderacion is not None:
        categoria.ponderacion = ponderacion
    if tipo_ponderacion is not None and tipo_ponderacion != categoria.tipo_ponderacion:
        categoria.tipo_ponderacion = tipo_ponderacion
        update_tipo_ponderacion_in_seccion(categoria.seccion_id, tipo_ponderacion)
    try:
        db.session.commit()
        if(percentage_sum_from_seccion_by_id(db.session, categoria.seccion_id)
            > MAX_PERCENTAGE and categoria.tipo_ponderacion == PERCENTAGE_TYPE):
            recalculate_seccion_ponderations(db.session, categoria.seccion_id)
        return categoria
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(BAD_REQUEST, description=f"Error al actualizar la categoría: {str(e)}")

def delete_categoria(categoria_id):
    categoria = get_categoria(categoria_id)
    if categoria:
        db.session.delete(categoria)
        db.session.commit()
        return True
    return False

def get_last_categoria_by_seccion_id( seccion_id ):
    return Categoria.query.filter_by(seccion_id=seccion_id).order_by(Categoria.id.desc()).first()

def validation_categoria(categoria, seccion_id):
    last_categoria = get_last_categoria_by_seccion_id(seccion_id)
    if last_categoria is None:
        return True
    return last_categoria.tipo_ponderacion == categoria.tipo_ponderacion

def update_tipo_ponderacion_in_seccion(seccion_id: int, nuevo_tipo: bool):
    categorias = get_all_categorias_by_seccion_id(seccion_id)
    for categoria in categorias:
        categoria.tipo_ponderacion = nuevo_tipo

    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(BAD_REQUEST, description=
        f"Error al actualizar tipo de ponderación en la sección: {str(e)}")

def create_multiple_categorias_and_evaluaciones(session: Session, seccion: Seccion,
                                                evaluacion_data: dict):
    for categoria_json in evaluacion_data.get("combinacion_topicos", []):
        categoria = create_categoria(
            seccion=seccion,
            tipo_categoria=categoria_json["nombre"],
            ponderacion=categoria_json["valor"],
            tipo_ponderacion=evaluacion_data.get("tipo") == "porcentaje"
        )

        evaluacion_topico = evaluacion_data.get("topicos", {}).get(str(categoria_json["id"]))
        if evaluacion_topico:
            valores = evaluacion_topico["valores"]
            tipo_ponderacion_actual = evaluacion_topico["tipo"] == "porcentaje"
            if tipo_ponderacion_actual:
                valores = prorate_values( evaluacion_topico["valores"] )
            for i in range(evaluacion_topico["cantidad"]):
                create_evaluacion(
                    session,
                    nombre=f"{categoria.tipo_categoria} {i + 1}",
                    ponderacion=valores[i],
                    opcional=not evaluacion_topico["obligatorias"][i],
                    tipo_ponderacion=tipo_ponderacion_actual,
                    categoria_id=categoria.id
                )