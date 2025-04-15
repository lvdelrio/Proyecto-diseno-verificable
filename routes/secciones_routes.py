from flask import Blueprint, request,  redirect, url_for, render_template
from db.config import db as config
from db.controller.seccion_controller import create_seccion, get_all_secciones_by_curso_id, get_all_secciones, get_seccion_by_id, edit_seccion_by_id, delete_seccion_by_id, curso_from_seccion_id

seccion_route_blueprint = Blueprint("Secciones", __name__)

@seccion_route_blueprint.route('/secciones/<int:curso_id>', methods=['POST'])
def add_seccion(curso_id):
    nombre = request.form["nombre_seccion"]

    nueva_seccion = create_seccion(config.session, curso_id, nombre)
    print("nueva_seccion", nueva_seccion)
    print(curso_id)

    return redirect(url_for("Cursos.view_curso", curso_id=curso_id, tab="secciones"))

@seccion_route_blueprint.route('/secciones', methods=['GET'])
def get_secciones_by_id(curso_id):
    secciones_by_curso_id = get_all_secciones_by_curso_id(config.session, curso_id)
    return redirect(url_for("Cursos.view_curso", secciones=secciones_by_curso_id))

@seccion_route_blueprint.route('/seccion/<int:seccion_id>')
def view_seccion(seccion_id):
    seccion = get_seccion_by_id(config.session, seccion_id)
    return render_template("secciones/detalle_seccion.html", seccion=seccion)

@seccion_route_blueprint.route('/editar_seccion/<int:seccion_id>', methods=['POST'])
def edit_seccion(seccion_id):
    nombre = request.form["nombre"]
    curso_id = curso_from_seccion_id(config.session, seccion_id)
    seccion = edit_seccion_by_id(config.session, seccion_id, nombre)
    
    return redirect(url_for("Cursos.view_curso", curso_id=curso_id))

@seccion_route_blueprint.route('/borrar_seccion/<int:seccion_id>', methods=['POST'])
def delete_seccion(seccion_id):
    curso_id = curso_from_seccion_id(config.session, seccion_id)
    delete_seccion_by_id(config.session, seccion_id)
    return redirect(url_for("Cursos.view_curso", curso_id=curso_id, tab="secciones"))