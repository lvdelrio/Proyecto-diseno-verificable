from flask import Blueprint, request, render_template, redirect, url_for, jsonify, abort
from db.config import db 
from db.controller.evaluacion_controller import (
    create_evaluacion,
    get_evaluacion_by_id,
    edit_evaluacion,
    delete_evaluacion, 
)
from utils.http_status import BAD_REQUEST, NOT_FOUND, BAD_REQUEST

evaluacion_blueprint = Blueprint("Evaluaciones", __name__)

@evaluacion_blueprint.route('/evaluaciones/add', methods=['POST'])
def add_evaluacion():
    try:
        categoria_id = request.form.get('categoria_id') 
        nombre = request.form.get('nombre')
        ponderacion = request.form.get('ponderacion')
        opcional = 'opcional' in request.form
        seccion_id = request.form.get('seccion_id')
        tipo_ponderacion = request.form.get('tipo_ponderacion')
        tipo_ponderacion = True if tipo_ponderacion == 'porcentaje' else False
        if any(value is None or (isinstance(value, str) and value.strip() == '')
            for value in [categoria_id, nombre, ponderacion, seccion_id]) or tipo_ponderacion is None:
            return redirect(url_for('Secciones.view_seccion', seccion_id=seccion_id, tab='evaluaciones'))
        
        try:
            ponderacion = float(ponderacion)
        except ValueError:
            return redirect(url_for('Secciones.view_seccion', seccion_id=seccion_id, tab='evaluaciones'))
        
        nueva_evaluacion = create_evaluacion(
            db=db.session,
            nombre=nombre,
            ponderacion=ponderacion,
            opcional=opcional,
            categoria_id=categoria_id, 
            tipo_ponderacion=tipo_ponderacion
        )
        
        return redirect(url_for('Secciones.view_seccion', seccion_id=seccion_id, tab='evaluaciones'))
    
    except Exception as e:
        db.session.rollback()
        return redirect(url_for('Secciones.view_seccion', seccion_id=seccion_id, tab='evaluaciones'))

@evaluacion_blueprint.route('/evaluaciones/<int:evaluacion_id>/notas')
def view_notas_evaluacion(evaluacion_id):
    evaluacion = get_evaluacion_by_id(db.session, evaluacion_id)
    if not evaluacion or not evaluacion.categoria or not evaluacion.categoria.seccion:
        return redirect(url_for('Cursos.get_cursos'))
    
    seccion_id = evaluacion.categoria.seccion.id
    return redirect(url_for('Secciones.view_seccion', seccion_id=seccion_id, tab='evaluaciones'))

@evaluacion_blueprint.route('/evaluaciones/<int:evaluacion_id>/delete', methods=['POST'])
def delete_evaluacion_route(evaluacion_id):
    try:
        evaluacion = get_evaluacion_by_id(db.session, evaluacion_id)
        seccion_id = evaluacion.categoria.seccion.id
        if not evaluacion or not evaluacion.categoria or not evaluacion.categoria.seccion:
            return jsonify({'success': False, 'message': 'Evaluación no encontrada'}), 404
        
        success = delete_evaluacion(db.session, evaluacion_id)
        if success:
            return redirect(url_for('Secciones.view_seccion', seccion_id=seccion_id, tab='evaluaciones'))
        
        return redirect(url_for('Secciones.view_seccion', seccion_id=seccion_id, tab='evaluaciones'))
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    
@evaluacion_blueprint.route('/evaluaciones/<int:evaluacion_id>/edit', methods=['GET'])
def edit_evaluacion_form(evaluacion_id):
    evaluacion = get_evaluacion_by_id(db.session, evaluacion_id)
    if not evaluacion:
        abort(NOT_FOUND, description="Evaluación no encontrada")

    return render_template('Secciones/partials/evaluaciones/edit_evaluacion.html', evaluacion=evaluacion, seccion=evaluacion.categoria.seccion)

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
    #CHANGE HER THIS LINE IS TOO LONG BUT DECIDED TO CHANGE WHEN WE ADD ERROR RESOLUTION
    if any(value is None or (isinstance(value, str) and value.strip() == '')
        for value in [categoria_id, nombre, ponderacion, seccion_id]) or tipo_ponderacion is None:
        abort(BAD_REQUEST, description="Faltan campos obligatorios")

    try:
        ponderacion = float(ponderacion)
    except ValueError:
        abort(BAD_REQUEST, description="La ponderación debe ser un número válido")


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
        abort(NOT_FOUND, description="Evaluación no encontrada")

    return redirect(url_for('Secciones.view_seccion', seccion_id=seccion_id, tab='evaluaciones'))
