from http import HTTPStatus
from flask import Blueprint, request, render_template, redirect, url_for, abort, jsonify
from db.config import db as config
from db.controller.notas_controller import (
    create_nota, get_nota_by_id, get_all_notas,
    delete_nota, load_notas_from_json
    )
from db.controller.alumno_controller import get_all_alumnos
from db.controller.evaluacion_controller import get_all_evaluaciones

nota_route_blueprint = Blueprint("Notas", __name__)
GET_NOTAS = "Notas.get_notas"

@nota_route_blueprint.route('/notas', methods=['GET'])
def get_notas():
    notas = get_all_notas(config.session)
    alumnos = get_all_alumnos(config.session)
    evaluaciones = get_all_evaluaciones(config.session)

    return render_template("Notas/notas.html",
                          notas=notas,
                          alumnos=alumnos,
                          evaluaciones=evaluaciones)

@nota_route_blueprint.route('/nota/<int:nota_id>')
def view_nota(nota_id):
    nota = get_nota_by_id(config.session, nota_id)
    check_nota_exists(nota)
    return render_template("Notas/detalle_nota.html", nota=nota)

@nota_route_blueprint.route('/agregar_nota', methods=['POST'])
def add_nota():
    alumno_id = request.form.get("alumno_id")
    evaluacion_id = request.form.get("evaluacion_id")
    nota_valor = request.form.get("nota")
    create_nota(config.session, alumno_id, evaluacion_id, nota_valor)
    return redirect(url_for(GET_NOTAS))

@nota_route_blueprint.route('/editar_nota/<int:nota_id>', methods=['POST'])
def edit_nota(nota_id):
    nota = get_nota_by_id(config.session, nota_id)
    check_nota_exists(nota)
    nota_valor = request.form.get("nota")
    create_nota(config.session, nota.alumno_id, nota.evaluacion_id, nota_valor)
    return redirect(url_for(GET_NOTAS))

@nota_route_blueprint.route('/borrar_nota/<int:nota_id>', methods=['POST'])
def delete_nota_route(nota_id):
    nota = get_nota_by_id(config.session, nota_id)
    check_nota_exists(nota)
    delete_nota(config.session, nota_id)
    return redirect(url_for(GET_NOTAS))

@nota_route_blueprint.route('/importar_notas', methods=['POST'])
def load_notas():
    data = request.json
    if not data:
        abort(HTTPStatus.BAD_REQUEST, description="No se recibió JSON válido.")
    load_notas_from_json(config.session, data)
    return jsonify({"message": "Notas importadas exitosamente."}), 201

def check_nota_exists(nota):
    if not nota:
        abort(HTTPStatus.NOT_FOUND, description="Nota no encontrada")
