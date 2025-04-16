from flask import Blueprint, request, redirect, url_for, render_template, abort
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
        curso_id = request.form.get('curso_id')
        
        tipo_ponderacion = request.form.get('tipo_ponderacion')
        tipo_ponderacion = True if tipo_ponderacion == 'porcentaje' else False
        
        seccion = db.session.query(Seccion).get(seccion_id)
        if not seccion:
            print('Sección no encontrada', 'error')
            return redirect(url_for('Cursos.view_curso', curso_id=curso_id, tab='evaluaciones'))
        
        nueva_categoria = create_categoria(
            tipo_categoria=tipo_categoria,
            seccion=seccion,
            ponderacion=ponderacion,
            tipo_ponderacion=tipo_ponderacion
        )
        
        print('Categoría creada exitosamente', 'success')
        return redirect(url_for('Cursos.view_curso', curso_id=curso_id, tab='evaluaciones'))
    
    except Exception as e:
        db.session.rollback()
        print(f'Error al crear categoría: {str(e)}', 'error')
        return redirect(url_for('Cursos.view_curso', curso_id=curso_id, tab='evaluaciones'))

@categoria_blueprint.route('/categorias/<int:categoria_id>/edit', methods=['GET'])
def edit_categoria_form(categoria_id):
    try:
        categoria = get_categoria(categoria_id)
        curso_id = categoria.seccion.curso_id 

        if not categoria:
            abort(404, description="Categoría no encontrada")

        curso_id = categoria.seccion.curso_id

        return render_template(
            'Cursos/partials/evaluaciones/edit_categoria.html',
            categoria=categoria,
            curso_id=curso_id,
            secciones=Seccion.query.filter_by(curso_id=curso_id).all()
        )
    except Exception as e:
        print(f'Error al cargar el formulario de edición: {str(e)}')
        abort(500, description="Error interno del servidor")

@categoria_blueprint.route('/categorias/<int:categoria_id>/edit', methods=['POST'])
def edit_categoria_route(categoria_id):
    try:
        tipo_categoria = request.form.get('tipo_categoria')
        ponderacion = float(request.form.get('ponderacion'))
        curso_id = request.form.get('curso_id')
        tipo_ponderacion = request.form.get('tipo_ponderacion')
        tipo_ponderacion = True if tipo_ponderacion == 'porcentaje' else False
        
        categoria = edit_categoria(
            categoria_id=categoria_id,
            tipo_categoria=tipo_categoria,
            ponderacion=ponderacion,
            tipo_ponderacion=tipo_ponderacion
        )
        
        print('Categoría actualizada exitosamente', 'success')
        return redirect(url_for('Cursos.view_curso', curso_id=curso_id, tab='evaluaciones'))
    
    except Exception as e:
        db.session.rollback()
        print(f'Error al actualizar categoría: {str(e)}', 'error')
        return redirect(url_for('Cursos.view_curso', curso_id=curso_id, tab='evaluaciones'))

@categoria_blueprint.route('/categorias/<int:categoria_id>/delete', methods=['POST'])
def delete_categoria_route(categoria_id):
    try:
        curso_id = request.form.get('curso_id')
        delete_categoria(categoria_id)
        print('Categoría eliminada exitosamente', 'success')
        return redirect(url_for('Cursos.view_curso', curso_id=curso_id, tab='evaluaciones'))
    
    except Exception as e:
        db.session.rollback()
        print(f'Error al eliminar categoría: {str(e)}', 'error')
        return redirect(url_for('Cursos.view_curso', curso_id=curso_id, tab='evaluaciones'))