from flask import abort
from sqlalchemy.orm import Session
from ..config import db
from ..models.categoria import Categoria
from ..models.seccion import Seccion
from ..controller.evaluacion_controller import create_evaluacion

def create_categoria(tipo_categoria, seccion, ponderacion, tipo_ponderacion):
    nueva_categoria = Categoria(
        tipo_categoria=tipo_categoria,
        id_seccion=seccion.id,
        ponderacion=ponderacion, 
        tipo_ponderacion=tipo_ponderacion
    )
    if not validation_categoria(nueva_categoria, seccion.id):
        db.session.rollback()
        abort(400, description="Error: La categoría no es válida para la sección.")
        return
    db.session.add(nueva_categoria)
    db.session.commit()
    return nueva_categoria

def get_categoria(categoria_id):
    return Categoria.query.get(categoria_id)

def edit_categoria(categoria_id, tipo_categoria=None, id_seccion=None, ponderacion=None, tipo_ponderacion=None):
    categoria = Categoria.query.get(categoria_id)
    if not categoria:
        abort(404, description="Categoría no encontrada")

    if tipo_categoria is not None:
        categoria.tipo_categoria = tipo_categoria
    if id_seccion is not None:
        categoria.id_seccion = id_seccion
    if ponderacion is not None:
        categoria.ponderacion = ponderacion
    if tipo_ponderacion is not None and tipo_ponderacion != categoria.tipo_ponderacion:
        categoria.tipo_ponderacion = tipo_ponderacion
        actualizar_tipo_ponderacion_en_seccion(categoria.id_seccion, tipo_ponderacion)

    try:
        db.session.commit()
        return categoria
    except Exception as e:
        db.session.rollback()
        abort(400, description=f"Error al actualizar la categoría: {str(e)}") 

def delete_categoria(categoria_id):
    categoria = Categoria.query.get(categoria_id)
    db.session.delete(categoria)
    db.session.commit()
    return

def get_last_categoria_by_seccion( seccion_id ):
    return Categoria.query.filter_by(id_seccion=seccion_id).order_by(Categoria.id.desc()).first()

def validation_categoria(categoria, seccion_id):
    last_category = get_last_categoria_by_seccion(seccion_id)
    if last_category is None:
        return True
    return last_category.tipo_ponderacion == categoria.tipo_ponderacion

def actualizar_tipo_ponderacion_en_seccion(seccion_id: int, nuevo_tipo: bool):
    categorias = Categoria.query.filter_by(id_seccion=seccion_id).all()
    for categoria in categorias:
        categoria.tipo_ponderacion = nuevo_tipo

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(400, description=f"Error al actualizar tipo de ponderación en la sección: {str(e)}")

def process_categorias(db: Session, seccion: Seccion, evaluacion_data: dict):
    tipo_ponderacion_global = evaluacion_data.get("tipo") == "porcentaje"

    for categoria_json in evaluacion_data.get("combinacion_topicos", []):
        categoria = create_categoria(
            seccion=seccion,
            tipo_categoria=categoria_json["nombre"],
            ponderacion=categoria_json["valor"],
            tipo_ponderacion=tipo_ponderacion_global
        )

        evaluaciones_json = evaluacion_data.get("topicos", {}).get(str(categoria_json["id"]), {})
        if evaluaciones_json:
            cantidad = evaluaciones_json["cantidad"]
            valores = evaluaciones_json["valores"]
            obligatorias = evaluaciones_json["obligatorias"]
            tipo_eval = evaluaciones_json["tipo"] == "porcentaje"

            for i in range(cantidad):
                create_evaluacion(
                    db,
                    nombre=f"{categoria.tipo_categoria} {i + 1}",
                    ponderacion=valores[i],
                    opcional=not obligatorias[i],
                    tipo_ponderacion=tipo_eval,
                    categoria_id=categoria.id
                )