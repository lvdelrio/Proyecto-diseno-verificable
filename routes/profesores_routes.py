from http import HTTPStatus
from flask import Blueprint, request, render_template, redirect, url_for, abort, jsonify
from db.config import db as config
from db.services.profesor_service import (
    get_profesor_and_available_cursos_with_secciones,
    register_profesor_in_seccion
    )
from db.controller.profesor_controller import (
    create_profesor,
    edit_profesor_by_id,
    delete_profesor_by_id,
    get_paginated_profesores,
    create_profesores_from_json,
    unregister_profesor_in_seccion
)

profesor_route_blueprint = Blueprint("Profesores", __name__)

@profesor_route_blueprint.route('/profesores', methods=['GET'])
@profesor_route_blueprint.route('/profesores/<int:pagina>', methods=['GET'])
def get_profesores(pagina=1):
    profesores_per_page = 10

    result_paging = get_paginated_profesores(
        session=config.session,
        page=pagina,
        per_page=profesores_per_page
    )

    return render_template(
        "Profesores/profesores.html",
        profesores=result_paging.items,
        pagina_actual=pagina,
        total_paginas=result_paging.pages,
        total_profesores=result_paging.total
    )

@profesor_route_blueprint.route('/profesor/<int:profesor_id>')
def view_profesor(profesor_id):
    profesor, cursos_with_secciones = get_profesor_and_available_cursos_with_secciones(config,
                                                                                       profesor_id)
    return render_template(
        "Profesores/detalle_profesor.html",
        profesor=profesor,
        cursos_con_secciones=cursos_with_secciones
    )

@profesor_route_blueprint.route('/agregar_profesor', methods=['POST'])
def add_profesor():
    nombre = request.form.get("nombre")
    email = request.form.get("email", "")
    profesor = create_profesor(config.session, nombre, email)
    return redirect(url_for("Profesores.view_profesor", profesor_id=profesor.id))

@profesor_route_blueprint.route('/editar_profesor/<int:profesor_id>', methods=['POST'])
def edit_profesor(profesor_id):
    nombre = request.form["nombre"]
    email = request.form["email"]
    edit_profesor_by_id(config.session, profesor_id, nombre, email)
    return redirect(url_for("Profesores.get_profesores"))

@profesor_route_blueprint.route('/borrar_profesor/<int:profesor_id>', methods=['POST'])
def delete_profesor(profesor_id):
    delete_profesor_by_id(config.session, profesor_id)
    return redirect(url_for("Profesores.get_profesores"))

@profesor_route_blueprint.route('/inscribir_profesor/<int:profesor_id>/', methods=['POST'])
def register_profesor(profesor_id):
    register_profesor_in_seccion(config.session, profesor_id, request.form)

    return redirect(url_for('Profesores.view_profesor', profesor_id=profesor_id))

@profesor_route_blueprint.route('/importar_profesores', methods=['POST'])
def load_profesores():
    data = request.json
    if not data:
        return jsonify({"message": "JSON vacío o inválido"}), HTTPStatus.BAD_REQUEST

    success, message = create_profesores_from_json(config.session, data)
    if not success:
        return jsonify({"message": message}), HTTPStatus.BAD_REQUEST
    return jsonify({"message": message}), HTTPStatus.CREATED

@profesor_route_blueprint.route('/desinscribir_profesor/<int:seccion_id>/', methods=['POST'])
def unregister_profesor(seccion_id):
    profesor_id = request.form.get("profesor_id")
    unregister_profesor_in_seccion(config.session, seccion_id, profesor_id)
    return redirect(url_for('Profesores.view_profesor', profesor_id=profesor_id))
