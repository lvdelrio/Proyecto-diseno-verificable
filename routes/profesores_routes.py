from flask import Blueprint, request, render_template, redirect, url_for
from db.config import db as config
from db.controller.profesor_controller import get_all_profesores, crear_profesor, get_profesor_by_id, edit_profesor_by_id, delete_profesor_by_id

profesor_route_blueprint = Blueprint("Profesores", __name__)

@profesor_route_blueprint.route('/profesores', methods=['GET'])
def get_profesores():
    profesores = get_all_profesores(config.session)
    return render_template("Profesores/profesores.html", profesores=profesores)

@profesor_route_blueprint.route('/profesor/<int:profesor_id>')
def view_profesor(profesor_id):
    profesor = get_profesor_by_id(config.session, profesor_id)
    print(profesor)
    return render_template("Profesores/detalle_profesor.html", profesor=profesor)

@profesor_route_blueprint.route('/agregar_profesor', methods=['POST'])
def add_profesor():
    nombre = request.form.get("nombre")
    email = request.form.get("email", "")
    print(nombre, email)
    profesor = crear_profesor(config.session, nombre, email)

    return redirect(url_for("Profesores.view_profesor", profesor_id=profesor.id))

@profesor_route_blueprint.route('/editar_profesor/<int:profesor_id>', methods=['POST'])
def edit_profesor(profesor_id):
    nombre = request.form["nombre"]
    email = request.form["email"]
    profesor = edit_profesor_by_id(config.session, profesor_id, nombre, email)
    
    return redirect(url_for("Profesores.get_profesores"))

@profesor_route_blueprint.route('/borrar_profesor/<int:profesor_id>', methods=['POST'])
def delete_profesor(profesor_id):
    delete_profesor_by_id(config.session, profesor_id)
    return redirect(url_for("Profesores.get_profesores"))

