from http import HTTPStatus
from flask import Blueprint, request, redirect, url_for, render_template, abort, flash
from db.config import db
from db.controller.categoria_controller import (
    create_categoria,
    get_categoria,
    edit_categoria,
    delete_categoria
)
from db.models.seccion import Seccion

SECCIONES_VIEW = 'Secciones.view_seccion'

categoria_blueprint = Blueprint("Categorias", __name__)

@categoria_blueprint.route('/categorias/add', methods=['POST'])
def add_categoria():
    try:
        tipo_categoria = request.form.get('tipo_categoria')
        seccion_id = request.form.get('seccion_id')
        ponderacion = float(request.form.get('ponderacion'))
        tipo_ponderacion = request.form.get('tipo_ponderacion')
        tipo_ponderacion = True if tipo_ponderacion == 'porcentaje' else False
        seccion = db.session.query(Seccion).get(seccion_id)
        if not seccion:
            print('Sección no encontrada', 'error')
            return redirect(url_for(SECCIONES_VIEW, seccion_id=seccion_id, tab='evaluaciones'))
        create_categoria(
            tipo_categoria=tipo_categoria,
            seccion=seccion,
            ponderacion=ponderacion,
            tipo_ponderacion=tipo_ponderacion
        )
        print('Categoría creada exitosamente', 'success')
        return redirect(url_for(SECCIONES_VIEW, seccion_id=seccion_id, tab='evaluaciones'))

    except Exception as e:
        db.session.rollback()
        flash(f"Ocurrió un error al crear la categoría: {str(e)}", "error")
        return redirect(url_for(SECCIONES_VIEW, seccion_id=seccion_id, tab='evaluaciones'))

@categoria_blueprint.route('/categorias/<int:categoria_id>/edit', methods=['GET'])
def edit_categoria_form(categoria_id):
    categoria = get_categoria(categoria_id)
    if not categoria:
        abort(HTTPStatus.NOT_FOUND, description="Categoría no encontrada")
    seccion_id = categoria.seccion.id
    return render_template(
        'secciones/partials/evaluaciones/edit_categoria.html',
        categoria=categoria,
        seccion_id=seccion_id
    )

@categoria_blueprint.route('/categorias/<int:categoria_id>/edit', methods=['POST'])
def edit_categoria_route(categoria_id):
    try:
        tipo_categoria = request.form.get('tipo_categoria')
        ponderacion = float(request.form.get('ponderacion'))
        seccion_id = request.form.get('seccion_id')
        tipo_ponderacion = request.form.get('tipo_ponderacion')
        tipo_ponderacion = True if tipo_ponderacion == 'porcentaje' else False

        edit_categoria(
            categoria_id=categoria_id,
            tipo_categoria=tipo_categoria,
            ponderacion=ponderacion,
            tipo_ponderacion=tipo_ponderacion
        )

        print('Categoría actualizada exitosamente', 'success')
        return redirect(url_for(SECCIONES_VIEW, seccion_id=seccion_id, tab='evaluaciones'))

    except Exception as e:
        db.session.rollback()
        flash(f"Ocurrió un error al editar la categoría: {str(e)}", "error")
        return redirect(url_for(SECCIONES_VIEW, seccion_id=seccion_id, tab='evaluaciones'))

@categoria_blueprint.route('/categorias/<int:categoria_id>/delete', methods=['POST'])
def delete_categoria_route(categoria_id):
    try:
        seccion_id = request.form.get('seccion_id')
        delete_categoria(categoria_id)
        print('Categoría eliminada exitosamente', 'success')
        return redirect(url_for(SECCIONES_VIEW, seccion_id=seccion_id, tab='evaluaciones'))

    except Exception as e:
        db.session.rollback()
        flash(f"Ocurrió un error al borrar la categoría: {str(e)}", "error")
        return redirect(url_for(SECCIONES_VIEW, seccion_id=seccion_id, tab='evaluaciones'))
