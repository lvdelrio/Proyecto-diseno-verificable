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
        categoria_id = request.form.get('categoria_id')  # Cambiamos de seccion_id a categoria_id
        tipo = request.form.get('tipo')
        ponderacion = request.form.get('ponderacion')
        opcional = 'opcional' in request.form
        curso_id = request.form.get('curso_id')
        
        if not all([categoria_id, tipo, ponderacion, curso_id]):
            print('Faltan campos obligatorios', 'error')
            return redirect(url_for('Cursos.view_curso', curso_id=curso_id, tab='evaluaciones'))
        
        try:
            ponderacion = float(ponderacion)
        except ValueError:
            print('La ponderación debe ser un número válido', 'error')
            return redirect(url_for('Cursos.view_curso', curso_id=curso_id, tab='evaluaciones'))
        
        # Usamos create_evaluacion_con_notas para crear notas vacías automáticamente
        nueva_evaluacion = create_evaluacion_con_notas(
            db=db.session,
            tipo=tipo,
            ponderacion=ponderacion,
            opcional=opcional,
            categoria_id=categoria_id
        )
        
        print('Evaluación creada exitosamente', 'success')
        return redirect(url_for('Cursos.view_curso', curso_id=curso_id, tab='evaluaciones'))
    
    except Exception as e:
        db.session.rollback()
        print(f'Error al crear evaluación: {str(e)}', 'error')
        return redirect(url_for('Cursos.view_curso', curso_id=curso_id, tab='evaluaciones'))