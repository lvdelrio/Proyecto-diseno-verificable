from http import HTTPStatus
from flask import Blueprint, request, render_template, redirect, url_for, jsonify, abort
from db.config import db
from db.controller.evaluacion_controller import (
    create_evaluacion,
    get_evaluacion_by_id,
    edit_evaluacion,
    delete_evaluacion,
)
from routes.utils.transform_methods import transform_to_float

evaluacion_blueprint = Blueprint("Evaluaciones", __name__)
SECCIONES_VIEW = 'Secciones.view_seccion'

@evaluacion_blueprint.route('/evaluaciones/add', methods=['POST'])
def add_evaluacion():
    try:
        form_data = extract_evaluacion_form_data()
        if not is_valid_evaluacion_data(form_data):
            return redirect_to_seccion_view(form_data['seccion_id'])
        ponderacion = transform_to_float(form_data['ponderacion'])
        if ponderacion is None:
            return redirect_to_seccion_view(form_data['seccion_id'])

        create_evaluacion(
            db=db.session,
            nombre=form_data['nombre'],
            ponderacion=ponderacion,
            opcional=form_data['opcional'],
            categoria_id=form_data['categoria_id'],
            tipo_ponderacion=form_data['tipo_ponderacion']
        )
        return redirect_to_seccion_view(form_data['seccion_id'])

    except Exception:
        db.session.rollback()
        return redirect_to_seccion_view(request.form.get('seccion_id'))

def extract_evaluacion_form_data():
    tipo_ponderacion_raw = request.form.get('tipo_ponderacion')
    return {
        'categoria_id': request.form.get('categoria_id'),
        'nombre': request.form.get('nombre'),
        'ponderacion': request.form.get('ponderacion'),
        'opcional': 'opcional' in request.form,
        'seccion_id': request.form.get('seccion_id'),
        'tipo_ponderacion': tipo_ponderacion_raw == 'porcentaje'
    }

def is_valid_evaluacion_data(form_data):
    required_fields = ['categoria_id', 'nombre', 'ponderacion', 'seccion_id']
    for field in required_fields:
        value = form_data[field]
        if value is None or (isinstance(value, str) and value.strip() == ''):
            return False

    return form_data['tipo_ponderacion'] is not None

def redirect_to_seccion_view(seccion_id):
    return redirect(url_for(SECCIONES_VIEW, seccion_id=seccion_id, tab='evaluaciones'))

@evaluacion_blueprint.route('/evaluaciones/<int:evaluacion_id>/notas')
def view_notas_evaluacion(evaluacion_id):
    evaluacion = get_evaluacion_by_id(db.session, evaluacion_id)
    if not evaluacion or not evaluacion.categoria or not evaluacion.categoria.seccion:
        return redirect(url_for('Cursos.get_cursos'))

    seccion_id = evaluacion.categoria.seccion.id
    return redirect(url_for(SECCIONES_VIEW, seccion_id=seccion_id, tab='evaluaciones'))

@evaluacion_blueprint.route('/evaluaciones/<int:evaluacion_id>/delete', methods=['POST'])
def delete_evaluacion_route(evaluacion_id):
    try:
        evaluacion = get_evaluacion_by_id(db.session, evaluacion_id)
        seccion_id = evaluacion.categoria.seccion.id
        if not evaluacion or not evaluacion.categoria or not evaluacion.categoria.seccion:
            return jsonify({'success': False, 'message': 'Evaluación no encontrada'}), 404

        success = delete_evaluacion(db.session, evaluacion_id)
        if success:
            return redirect(url_for(SECCIONES_VIEW, seccion_id=seccion_id, tab='evaluaciones'))

        return redirect(url_for(SECCIONES_VIEW, seccion_id=seccion_id, tab='evaluaciones'))

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@evaluacion_blueprint.route('/evaluaciones/<int:evaluacion_id>/edit', methods=['GET'])
def edit_evaluacion_form(evaluacion_id):
    evaluacion = get_evaluacion_by_id(db.session, evaluacion_id)
    if not evaluacion:
        abort(HTTPStatus.NOT_FOUND, description="Evaluación no encontrada")

    return render_template('Secciones/partials/evaluaciones/edit_evaluacion.html',
                           evaluacion=evaluacion, seccion=evaluacion.categoria.seccion)

@evaluacion_blueprint.route('/evaluaciones/<int:evaluacion_id>/edit', methods=['POST'])
def edit_evaluacion_route(evaluacion_id):
    evaluacion = get_evaluacion_by_id(db.session, evaluacion_id)
    seccion_id = evaluacion.categoria.seccion.id

    nombre = request.form.get('nombre')
    ponderacion = request.form.get('ponderacion')
    opcional = 'opcional' in request.form
    categoria_id = request.form.get('categoria_id')
    tipo_ponderacion = request.form.get('tipo_ponderacion')
    tipo_ponderacion = True if tipo_ponderacion == 'porcentaje' else False
    if any(value is None or (isinstance(value, str) and value.strip() == '')
        for value in [categoria_id, nombre, ponderacion, seccion_id]) or tipo_ponderacion is None:
        abort(HTTPStatus.BAD_REQUEST, description="Faltan campos obligatorios")

    try:
        ponderacion = float(ponderacion)
    except ValueError:
        abort(HTTPStatus.BAD_REQUEST, description="La ponderación debe ser un número válido")


    evaluacion = edit_evaluacion(
        db.session,
        evaluacion_id=evaluacion_id,
        nombre=nombre,
        ponderacion=ponderacion,
        opcional=opcional,
        categoria_id=categoria_id,
        tipo_ponderacion=tipo_ponderacion
    )

    if not evaluacion:
        abort(HTTPStatus.NOT_FOUND, description="Evaluación no encontrada")

    return redirect(url_for(SECCIONES_VIEW, seccion_id=seccion_id, tab='evaluaciones'))
