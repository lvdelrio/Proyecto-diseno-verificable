from flask import Blueprint, request, redirect, url_for, flash
from db.config import db
from db.controller.categoria_controller import (
    create_categoria,
    get_categoria,
    edit_categoria,
    delete_categoria
)
from db.models.seccion import Seccion

categoria_blueprint = Blueprint("Categorias", __name__)

@categoria_blueprint.route('/categorias/add', methods=['POST'])
def add_categoria():
    try:
        tipo_categoria = request.form.get('tipo_categoria')
        seccion_id = request.form.get('seccion_id')
        ponderacion = float(request.form.get('ponderacion'))
        opcional = 'opcional' in request.form
        curso_id = request.form.get('curso_id')
        
        seccion = db.session.query(Seccion).get(seccion_id)
        if not seccion:
            flash('Sección no encontrada', 'error')
            return redirect(url_for('Cursos.view_curso', curso_id=curso_id, tab='evaluaciones'))
        
        nueva_categoria = create_categoria(
            tipo_categoria=tipo_categoria,
            seccion=seccion,
            ponderacion=ponderacion,
            opcional=opcional
        )
        
        flash('Categoría creada exitosamente', 'success')
        return redirect(url_for('Cursos.view_curso', curso_id=curso_id, tab='evaluaciones'))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error al crear categoría: {str(e)}', 'error')
        return redirect(url_for('Cursos.view_curso', curso_id=curso_id, tab='evaluaciones'))

@categoria_blueprint.route('/categorias/<int:categoria_id>/edit', methods=['POST'])
def edit_categoria_route(categoria_id):
    try:
        tipo_categoria = request.form.get('tipo_categoria')
        ponderacion = float(request.form.get('ponderacion'))
        opcional = 'opcional' in request.form
        curso_id = request.form.get('curso_id')
        
        categoria = edit_categoria(
            categoria_id=categoria_id,
            tipo_categoria=tipo_categoria,
            ponderacion=ponderacion,
            opcional=opcional
        )
        
        flash('Categoría actualizada exitosamente', 'success')
        return redirect(url_for('Cursos.view_curso', curso_id=curso_id, tab='evaluaciones'))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error al actualizar categoría: {str(e)}', 'error')
        return redirect(url_for('Cursos.view_curso', curso_id=curso_id, tab='evaluaciones'))

@categoria_blueprint.route('/categorias/<int:categoria_id>/delete', methods=['POST'])
def delete_categoria_route(categoria_id):
    try:
        curso_id = request.form.get('curso_id')
        delete_categoria(categoria_id)
        flash('Categoría eliminada exitosamente', 'success')
        return redirect(url_for('Cursos.view_curso', curso_id=curso_id, tab='evaluaciones'))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar categoría: {str(e)}', 'error')
        return redirect(url_for('Cursos.view_curso', curso_id=curso_id, tab='evaluaciones'))