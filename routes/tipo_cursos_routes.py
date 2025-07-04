from http import HTTPStatus
from flask import Blueprint, request, render_template, redirect, url_for, abort, jsonify
from db.config import db as config
from db.controller.tipo_curso_controller import (
    get_all_tipo_cursos,
    create_tipo_curso,
    edit_tipo_curso_by_id,
    delete_tipo_curso_by_id,
    create_tipo_cursos_from_json
    )
from db.services.tipo_curso_service import (
    get_tipo_curso_and_cursos_disponibles,
    register_tipo_curso_in_tipo_cursos
    )

tipo_curso_route_blueprint = Blueprint("Tipo_Cursos", __name__)

@tipo_curso_route_blueprint.route('/tipo_cursos', methods=['GET'])
def get_tipo_cursos():
    tipo_cursos = get_all_tipo_cursos(config.session)
    return render_template("tipo_cursos/tipo_cursos.html", tipo_cursos=tipo_cursos)

@tipo_curso_route_blueprint.route('/tipo_curso/<int:tipo_curso_id>')
def view_tipo_curso(tipo_curso_id):
    tipo_curso_base, cursos_disponibles = get_tipo_curso_and_cursos_disponibles(config,
                                                                                 tipo_curso_id)
    return render_template(
        "Tipo_Cursos/detalle_tipo_curso.html",
        tipo_curso=tipo_curso_base,
        tipo_cursos_disponibles=cursos_disponibles
    )

@tipo_curso_route_blueprint.route('/agregar_tipo_curso', methods=['POST'])
def add_tipo_curso():
    tipo_curso_code = request.form.get("codigo")
    description = request.form.get("descripcion", "")
    tipo_curso_credits = request.form.get("credits", "")
    tipo_curso = create_tipo_curso(config.session, tipo_curso_code, description, tipo_curso_credits)
    return redirect(url_for("Tipo_Cursos.view_tipo_curso", tipo_curso_id=tipo_curso.id))

@tipo_curso_route_blueprint.route('/editar_tipo_curso/<int:tipo_curso_id>', methods=['POST'])
def edit_tipo_curso(tipo_curso_id):
    tipo_curso_code = request.form["codigo"]
    description = request.form["descripcion"]
    edit_tipo_curso_by_id(config.session, tipo_curso_id, tipo_curso_code, description)
    return redirect(url_for("Tipo_Cursos.get_tipo_cursos"))

@tipo_curso_route_blueprint.route('/borrar_tipo_curso/<int:tipo_curso_id>', methods=['POST'])
def delete_tipo_curso(tipo_curso_id):
    delete_tipo_curso_by_id(config.session, tipo_curso_id)
    return redirect(url_for("Tipo_Cursos.get_tipo_cursos"))

@tipo_curso_route_blueprint.route('/inscribir_curso/<int:tipo_curso_id>/', methods=['POST'])
def register_tipo_curso(tipo_curso_id):
    register_tipo_curso_in_tipo_cursos(config.session, tipo_curso_id, request.form)
    return redirect(url_for('Tipo_Cursos.view_tipo_curso', tipo_curso_id=tipo_curso_id))

@tipo_curso_route_blueprint.route("/importar_tipo_cursos", methods=["POST"])
def load_tipo_cursos():
    data = request.json
    if not data:
        return jsonify({"message": "JSON vacío o inválido"}), HTTPStatus.BAD_REQUEST,

    success, message = create_tipo_cursos_from_json(config.session, data)
    if not success:
        return jsonify({"message": message}), HTTPStatus.BAD_REQUEST,
    return jsonify({"message": message}), HTTPStatus.CREATED
