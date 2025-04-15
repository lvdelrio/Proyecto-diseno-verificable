# routes/evaluacion_routes.py
from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from db.config import db as config
from db.controller.evaluacion_controller import (
    create_evaluacion,
    get_evaluacion_by_id,
    get_evaluaciones_by_seccion,
    update_evaluacion,
    delete_evaluacion
)
from db.controller.notas_controller import get_notas_by_evaluacion

evaluacion_blueprint = Blueprint("Evaluaciones", __name__)

@evaluacion_blueprint.route('/evaluaciones/add', methods=['POST'])
def add_evaluacion():
    seccion_id = request.form.get('seccion_id')
    tipo = request.form.get('tipo')
    ponderacion = float(request.form.get('ponderacion'))
    opcional = 'opcional' in request.form
    curso_id = request.form.get('curso_id')
    
    nueva_evaluacion = create_evaluacion(config.session,tipo,
                                         ponderacion,opcional,
                                         seccion_id)
    print(nueva_evaluacion)
    return redirect(url_for('Cursos.view_curso', curso_id=curso_id, tab='evaluaciones'))

@evaluacion_blueprint.route('/evaluaciones/<int:evaluacion_id>/delete', methods=['POST'])
def delete_evaluacion(evaluacion_id):
    delete_evaluacion(config.session, evaluacion_id)
    return jsonify({'success': True})

@evaluacion_blueprint.route('/evaluaciones/<int:evaluacion_id>/notas')
def view_notas_evaluacion(evaluacion_id):
    evaluacion = get_evaluacion_by_id(config.session, evaluacion_id)
    notas = get_notas_by_evaluacion(config.session, evaluacion_id)
    return render_template(
        'Evaluaciones/notas_evaluacion.html',
        evaluacion=evaluacion,
        notas=notas
    )