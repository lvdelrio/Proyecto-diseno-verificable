from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from db.config import db 
from db.controller.evaluacion_controller import (
    create_evaluacion,
    get_evaluacion_by_id,
    get_evaluaciones_by_seccion,
    edit_evaluacion,
    delete_evaluacion, 
    create_evaluacion_con_notas
)
from db.controller.notas_controller import get_notas_by_evaluacion

evaluacion_blueprint = Blueprint("Evaluaciones", __name__)

@evaluacion_blueprint.route('/evaluaciones/add', methods=['POST'])
def add_evaluacion():
    try:
        categoria_id = request.form.get('categoria_id') 
        nombre = request.form.get('nombre')
        ponderacion = request.form.get('ponderacion')
        opcional = 'opcional' in request.form
        curso_id = request.form.get('curso_id')
        tipo_ponderacion = request.form.get('tipo_ponderacion')
        tipo_ponderacion = True if tipo_ponderacion == 'porcentaje' else False

        if any(value is None or (isinstance(value, str) and value.strip() == '') for value in [categoria_id, nombre, ponderacion, curso_id]) or tipo_ponderacion is None:
            print('Faltan campos obligatorios', 'error')
            return redirect(url_for('Cursos.view_curso', curso_id=curso_id, tab='evaluaciones'))
        
        try:
            ponderacion = float(ponderacion)
        except ValueError:
            print('La ponderación debe ser un número válido', 'error')
            return redirect(url_for('Cursos.view_curso', curso_id=curso_id, tab='evaluaciones'))
        
        nueva_evaluacion = create_evaluacion(
            db=db.session,
            nombre=nombre,
            ponderacion=ponderacion,
            opcional=opcional,
            categoria_id=categoria_id, 
            tipo_ponderacion=tipo_ponderacion
        )
        
        print('Evaluación creada exitosamente', 'success')
        return redirect(url_for('Cursos.view_curso', curso_id=curso_id, tab='evaluaciones'))
    
    except Exception as e:
        db.session.rollback()
        print(f'Error al crear evaluación: {str(e)}', 'error')
        return redirect(url_for('Cursos.view_curso', curso_id=curso_id, tab='evaluaciones'))

@evaluacion_blueprint.route('/evaluaciones/<int:evaluacion_id>/notas')
def view_notas_evaluacion(evaluacion_id):
    evaluacion = get_evaluacion_by_id(db.session, evaluacion_id)
    if not evaluacion or not evaluacion.categoria or not evaluacion.categoria.seccion:
        return redirect(url_for('Cursos.get_cursos'))
    
    curso_id = evaluacion.categoria.seccion.curso_id
    return redirect(url_for('Cursos.view_curso', curso_id=curso_id, tab='evaluaciones'))

@evaluacion_blueprint.route('/evaluaciones/<int:evaluacion_id>/delete', methods=['POST'])
def delete_evaluacion_route(evaluacion_id):
    try:
        evaluacion = get_evaluacion_by_id(db.session, evaluacion_id)
        curso_id = evaluacion.categoria.seccion.curso_id
        if not evaluacion or not evaluacion.categoria or not evaluacion.categoria.seccion:
            return jsonify({'success': False, 'message': 'Evaluación no encontrada'}), 404
        
        success = delete_evaluacion(db.session, evaluacion_id)
        if success:
            return jsonify({
                'success': True,
                'message': 'Evaluación eliminada',
                'redirect': url_for('Cursos.view_curso', curso_id=curso_id, tab='evaluaciones')
            })
        return jsonify({'success': False, 'message': 'No se pudo eliminar la evaluación'}), 400
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500