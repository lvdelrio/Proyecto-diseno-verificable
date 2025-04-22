from flask import Blueprint, request, jsonify
from db.controller.sala_controller import create_sala, get_all_salas, delete_sala, load_salas_from_json, edit_sala_by_id
from db.config import db as config

sala_route_blueprint = Blueprint("Salas", __name__)

@sala_route_blueprint.route("/agregar_sala", methods=["POST"])
def add_sala():
    data = request.json
    sala = create_sala(config.session, data["nombre"], data["capacidad"])
    return jsonify({"id": sala.id, "nombre": sala.nombre, "capacidad": sala.capacidad}), 201

@sala_route_blueprint.route("/sala/<int:sala_id>", methods=["GET"])
def get_sala(sala_id):
    sala = get_all_salas(config.session, sala_id)
    if sala:
        return jsonify({"id": sala.id, "nombre": sala.nombre, "capacidad": sala.capacidad}), 200
    return jsonify({"error": "Sala no encontrada"}), 404


@sala_route_blueprint.route("/salas", methods=["GET"])
def get_salas():
    salas = get_all_salas(config.session)
    return jsonify([{"id": sala.id, "nombre": sala.nombre, "capacidad": sala.capacidad} for sala in salas]), 200

@sala_route_blueprint.route("/editar_sala", methods=["GET"])
def edit_sala(sala_id):
    nombre = request.form.get("nombre")
    capacidad = request.form.get("capacidad")
    sala = edit_sala_by_id(config.session, sala_id, nombre, capacidad)
    if sala:
        return jsonify({"id": sala.id, "nombre": sala.nombre, "capacidad": sala.capacidad}), 200
    return jsonify({"error": "Sala no encontrada"}), 404

@sala_route_blueprint.route("/borrar_sala/<int:sala_id>", methods=["DELETE"])
def delete_sala(sala_id):
    success = delete_sala(config.session, sala_id)
    if success:
        return jsonify({"message": "Sala eliminada"}), 200
    return jsonify({"error": "Sala no encontrada"}), 404

@sala_route_blueprint.route("/importar_salas", methods=["POST"])
def load_salas():
    data = request.get_json()
    load_salas_from_json(config.session, data)
    return jsonify({"message": "Salas importadas exitosamente."}), 201