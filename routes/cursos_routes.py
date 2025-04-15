from flask import Blueprint, request, render_template, redirect, url_for
from db.config import db as config
from db.controller.curso_controller import get_all_cursos, create_curso, get_curso_by_id, edit_curso_by_id, delete_curso_by_id

curso_route_blueprint = Blueprint("Cursos", __name__)

@curso_route_blueprint.route('/cursos', methods=['GET'])
def get_cursos():
    cursos = get_all_cursos(config.session)
    return render_template("Cursos/cursos.html", cursos=cursos)

@curso_route_blueprint.route('/curso/<int:curso_id>')
def view_curso(curso_id):
    curso = get_curso_by_id(config.session, curso_id)
    return render_template("Cursos/detalle_curso.html", curso=curso)

@curso_route_blueprint.route('/agregar_curso', methods=['POST'])
def add_curso():
    name = request.form.get("nombre")
    description = request.form.get("descripcion", "")
    semestre_de_ejecucion =request.form.get("semestre_de_ejecucion")
    course = create_curso(config.session, name, description, semestre_de_ejecucion)

    return redirect(url_for("Cursos.view_curso", curso_id=course.id))

@curso_route_blueprint.route('/editar_curso/<int:curso_id>', methods=['POST'])
def edit_curso(curso_id):
    name = request.form["nombre"]
    description = request.form["descripcion"]
    semestre_de_ejecucion = request.form["semestre_de_ejecucion"]
    curso = edit_curso_by_id(config.session, curso_id, name, description, semestre_de_ejecucion)
    
    return redirect(url_for("Cursos.get_cursos"))

@curso_route_blueprint.route('/borrar_curso/<int:curso_id>', methods=['POST'])
def delete_curso(curso_id):
    delete_curso_by_id(config.session, curso_id)
    return redirect(url_for("Cursos.get_cursos"))