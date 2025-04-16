from flask import Blueprint, request, render_template, redirect, url_for, abort
from db.config import db as config
from db.controller.tipo_curso_controller import get_all_tipo_cursos, create_tipo_curso, get_tipo_curso_by_id, edit_tipo_curso_by_id, delete_tipo_curso_by_id, enroll_tipo_curso_in_tipo_cursos

tipo_curso_route_blueprint = Blueprint("Tipo_Cursos", __name__)

@tipo_curso_route_blueprint.route('/tipo_cursos', methods=['GET'])
def get_tipo_cursos():
    tipo_cursos = get_all_tipo_cursos(config.session)
    return render_template("tipo_cursos/tipo_cursos.html", tipo_cursos=tipo_cursos)

@tipo_curso_route_blueprint.route('/tipo_curso/<int:tipo_curso_id>')
def view_tipo_curso(tipo_curso_id):
    tipo_curso_base = get_tipo_curso_by_id(config.session, tipo_curso_id)

    if tipo_curso_base is None:
        abort(404, description="Tipo curso no encontrado.")

    tipo_cursos_inscritos_ids = {
        requisito.curso_requisito.id
        for requisito in tipo_curso_base.requisitos
        if requisito.curso_requisito is not None
    }
    cursos_disponibles = [
        curso for curso in get_all_tipo_cursos(config.session)
        if curso.id not in tipo_cursos_inscritos_ids and curso.id != tipo_curso_id
    ]

    return render_template(
        "Tipo_Cursos/detalle_tipo_curso.html",
        tipo_curso=tipo_curso_base,
        tipo_cursos_disponibles=cursos_disponibles
    )

@tipo_curso_route_blueprint.route('/agregar_tipo_curso', methods=['POST'])
def add_tipo_curso():
    name = request.form.get("nombre")
    description = request.form.get("descripcion", "")
    tipo_curso = create_tipo_curso(config.session, name, description)

    return redirect(url_for("Tipo_Cursos.view_tipo_curso", tipo_curso_id=tipo_curso.id))

@tipo_curso_route_blueprint.route('/editar_tipo_curso/<int:tipo_curso_id>', methods=['POST'])
def edit_tipo_curso(tipo_curso_id):
    name = request.form["nombre"]
    description = request.form["descripcion"]
    tipo_curso = edit_tipo_curso_by_id(config.session, tipo_curso_id, name, description)
    
    return redirect(url_for("Tipo_Cursos.get_tipo_cursos"))

@tipo_curso_route_blueprint.route('/borrar_tipo_curso/<int:tipo_curso_id>', methods=['POST'])
def delete_tipo_curso(tipo_curso_id):
    delete_tipo_curso_by_id(config.session, tipo_curso_id)
    return redirect(url_for("Tipo_Cursos.get_tipo_cursos"))

@tipo_curso_route_blueprint.route('/inscribir/<int:tipo_curso_id>/', methods=['POST'])
def inscribir_tipo_curso(tipo_curso_id):
    tipo_curso_by_id = get_tipo_curso_by_id(config.session, tipo_curso_id)
    tipo_cursos_ids = request.form.getlist("tipo_curso_ids")  # <-- Get all checked checkboxes

    enrolled_tipo_cursos = []
    errors = []

    for tipo_id in tipo_cursos_ids:
        exito, mensaje = enroll_tipo_curso_in_tipo_cursos(config.session, tipo_curso_id, int(tipo_id))
        if exito:
            enrolled_tipo_cursos.append(mensaje)
        else:
            errors.append(mensaje)

    return redirect(url_for('Tipo_Cursos.view_tipo_curso', tipo_curso_id=tipo_curso_id))
