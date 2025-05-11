from flask import Blueprint, render_template, request, jsonify, redirect, url_for, abort
from db.controller.sala_controller import create_sala, get_all_salas, get_sala_by_id, delete_sala, load_salas_from_json, edit_sala_by_id
from db.config import db as config

sala_route_blueprint = Blueprint("Salas", __name__)

@sala_route_blueprint.route("/agregar_sala", methods=["POST"])
def add_sala():
    nombre = request.form.get("nombre")
    capacidad = request.form.get("capacidad")
    sala = create_sala(config.session, nombre, capacidad)
    return redirect(url_for("Salas.view_sala", sala_id=sala.id))

@sala_route_blueprint.route("/salas/<int:sala_id>", methods=["GET"])
def view_sala(sala_id):
    sala = get_sala_by_id(config.session, sala_id)
    if not sala:
        abort(404, description="Sala no encontrada")
    return render_template("Salas/detalle_sala.html", sala=sala)

@sala_route_blueprint.route("/sala/<int:sala_id>", methods=["GET"])
def get_sala(sala_id):
    sala = get_all_salas(config.session, sala_id)
    if sala:
        return jsonify({"id": sala.id, "nombre": sala.nombre, "capacidad": sala.capacidad}), 200
    return jsonify({"error": "Sala no encontrada"}), 404


@sala_route_blueprint.route("/salas", methods=["GET"])
def get_salas():
    salas = get_all_salas(config.session)
    return render_template("Salas/salas.html", salas=salas)

@sala_route_blueprint.route('/editar_sala/<int:sala_id>', methods=['POST'])
def edit_sala(sala_id):
    nombre = request.form.get("nombre")
    capacidad = request.form.get("capacidad")
    sala = edit_sala_by_id(config.session, sala_id, nombre, capacidad)
    
    return redirect(url_for("Salas.get_salas"))

@sala_route_blueprint.route('/borrar_sala/<int:sala_id>', methods=['POST'])
def delete_sala_route(sala_id):
    delete_sala(config.session, sala_id)
    return redirect(url_for("Salas.get_salas"))

@sala_route_blueprint.route("/importar_salas", methods=["POST"])
def load_salas():
    data = request.get_json()
    load_salas_from_json(config.session, data)
    return jsonify({"message": "Salas importadas exitosamente."}), 201