from flask import Blueprint, request, render_template, redirect, url_for, abort, jsonify, flash
from db.config import db as config
from db.controller.tipo_curso_controller import get_all_tipo_cursos
from db.controller.curso_controller import get_all_cursos, create_curso, get_curso_by_id, edit_curso_by_id, delete_curso_by_id, create_cursos_from_json, cerrar_curso, abrir_curso
from db.controller.alumno_controller import create_alumno_seccion_from_json
curso_route_blueprint = Blueprint("Cursos", __name__)

@curso_route_blueprint.route('/cursos', methods=['GET'])
def get_cursos():
    cursos = get_all_cursos(config.session)
    tipo_cursos = get_all_tipo_cursos(config.session)
    return render_template("Cursos/cursos.html", cursos=cursos, tipo_cursos=tipo_cursos)

@curso_route_blueprint.route('/curso/<int:curso_id>')
def view_curso(curso_id):
    curso = get_curso_by_id(config.session, curso_id)
    return render_template("Cursos/detalle_curso.html", curso=curso)

@curso_route_blueprint.route('/agregar_curso', methods=['POST'])
def add_curso():
    id_tipo_curso = request.form.get("tipo_curso_id")
    imparted_fecha = request.form.get("fecha_impartida")
    imparted_semester = request.form.get("semestre_impartido")
    curso = create_curso(config.session, id_tipo_curso, imparted_fecha, imparted_semester)

    return redirect(url_for("Cursos.view_curso", curso_id=curso.id))

@curso_route_blueprint.route('/editar_curso/<int:curso_id>', methods=['POST'])
def edit_curso(curso_id):
    curso = get_curso_by_id(config.session, curso_id)
    imparted_fecha = request.form["fecha_impartida"]
    imparted_semester = request.form["semestre_impartido"]
    curso = edit_curso_by_id(config.session, curso_id, curso.tipo_curso.id, imparted_fecha, imparted_semester)
    
    return redirect(url_for("Cursos.get_cursos"))

@curso_route_blueprint.route('/borrar_curso/<int:curso_id>', methods=['POST'])
def delete_curso(curso_id):
    delete_curso_by_id(config.session, curso_id)
    return redirect(url_for("Cursos.get_cursos"))

@curso_route_blueprint.route("/importar_cursos", methods=["POST"])
def load_cursos():
    data = request.json
    if not data:
        abort(400, description="No se recibió JSON válido.")

    create_cursos_from_json(config.session, data)
    return jsonify({"message": "Cursos cargados correctamente"}), 201

@curso_route_blueprint.route("/imporar_alumno_in_seccion", methods=["POST"])
def load_alumno_in_seccion():
    data = request.json
    if not data:
        abort(400, description="No se recibió JSON válido.")
    
    create_alumno_seccion_from_json(config.session, data)
    return jsonify({"message": "Alumnos inscritos correctamente"}), 201

@curso_route_blueprint.route('/curso/<int:curso_id>/toggle_estado', methods=['POST'])
def toggle_curso_estado(curso_id):
    curso = get_curso_by_id(config.session, curso_id)
    if not curso:
        abort(404, description="Curso no encontrado")
    
    if curso.cerrado:
        abrir_curso(config.session, curso_id)
    else:
        cerrar_curso(config.session, curso_id)
    
    return redirect(url_for("Cursos.view_curso", curso_id=curso_id))