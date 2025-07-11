from http import HTTPStatus
from flask import Blueprint, request,  redirect, url_for, render_template, abort, jsonify
from db.config import db as config
from db.controller.common_controller import get_seccion_by_id
from db.controller.seccion_controller import (
    create_seccion,
    get_all_secciones_by_curso_id,
    delete_seccion_by_id,
    curso_from_seccion_id,
    create_secciones_from_json
    )

CURSOS_VIEW = "Cursos.view_curso"

seccion_route_blueprint = Blueprint("Secciones", __name__)

@seccion_route_blueprint.route('/secciones/<int:curso_id>', methods=['POST'])
def add_seccion(curso_id):
    nombre = request.form["nombre_seccion"]
    create_seccion(config.session, curso_id, nombre)
    return redirect(url_for(CURSOS_VIEW, curso_id=curso_id, tab="secciones"))

@seccion_route_blueprint.route('/secciones', methods=['GET'])
def get_secciones_by_id(curso_id):
    secciones_by_curso_id = get_all_secciones_by_curso_id(config.session, curso_id)
    return redirect(url_for(CURSOS_VIEW, secciones=secciones_by_curso_id))

@seccion_route_blueprint.route('/seccion/<int:seccion_id>')
def view_seccion(seccion_id):
    seccion = get_seccion_by_id(config.session, seccion_id)
    return render_template("secciones/detalle_seccion.html", seccion=seccion, tab="info")

@seccion_route_blueprint.route('/editar_seccion/<int:seccion_id>', methods=['POST'])
def edit_seccion(seccion_id):
    curso_id = curso_from_seccion_id(config.session, seccion_id)
    return redirect(url_for(CURSOS_VIEW, curso_id=curso_id))

@seccion_route_blueprint.route('/borrar_seccion/<int:seccion_id>', methods=['POST'])
def delete_seccion(seccion_id):
    curso_id = curso_from_seccion_id(config.session, seccion_id)
    delete_seccion_by_id(config.session, seccion_id)
    return redirect(url_for(CURSOS_VIEW, curso_id=curso_id, tab="secciones"))

@seccion_route_blueprint.route('/importar_secciones', methods=['POST'])
def importar_secciones():
    data = request.json
    if not data:
        return jsonify({"message": "JSON vacío o inválido"}), HTTPStatus.BAD_REQUEST

    success, message = create_secciones_from_json(config.session, data)
    if not success:
        return jsonify({"message": message}), HTTPStatus.BAD_REQUEST
    return jsonify({"message": message}), HTTPStatus.CREATED
