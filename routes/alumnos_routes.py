from flask import Blueprint, request, render_template, redirect, url_for, flash, abort, jsonify
from flask import Blueprint, request, render_template, redirect, url_for, flash, abort, jsonify
from db.config import db as config
from db.controller.curso_controller import get_all_cursos
from db.controller.seccion_controller import get_all_secciones_by_curso_id
from db.services.alumno_service import get_available_cursos_con_secciones, register_alumno_in_secciones
from db.controller.alumno_controller import (
    get_all_alumnos,
    create_alumno,
    get_alumno_by_id,
    edit_alumno_by_id,
    delete_alumno_by_id,
    get_paginated_alumnos,
    create_alumnos_from_json,
    unregister_alumno_in_seccion
)
from utils.http_status import BAD_REQUEST, NOT_FOUND
alumno_route_blueprint = Blueprint("Alumnos", __name__)

@alumno_route_blueprint.route('/alumnos')
@alumno_route_blueprint.route('/alumnos/<int:pagina>')
def get_alumnos(pagina=1):
    alumnos_per_page = 10

    result_paging = get_paginated_alumnos(
        session=config.session,  
        page=pagina,
        per_page=alumnos_per_page
    )
    
    return render_template(
        "Alumnos/alumnos.html",
        alumnos=result_paging.items,       
        pagina_actual=pagina,                   
        total_paginas=result_paging.pages, 
        total_alumnos=result_paging.total  
    )

@alumno_route_blueprint.route('/alumno/<int:alumno_id>')
def view_alumno(alumno_id):
    alumno, cursos_with_secciones = get_available_cursos_con_secciones(config, alumno_id)
    if alumno is None:
        abort(NOT_FOUND, description="Alumno no encontrado.")

    return render_template(
        "Alumnos/detalle_alumno.html",
        alumno=alumno,
        cursos_con_secciones=cursos_with_secciones
    )

@alumno_route_blueprint.route('/agregar_alumno', methods=['POST'])
def add_alumno():
    nombre = request.form.get("nombre")
    email = request.form.get("email")
    fecha_ingreso = request.form.get("fecha_ingreso")
    
    alumno = create_alumno(config.session, nombre, email, fecha_ingreso)
    return redirect(url_for("Alumnos.view_alumno", alumno_id=alumno.id))

@alumno_route_blueprint.route('/editar_alumno/<int:alumno_id>', methods=['POST'])
def edit_alumno(alumno_id):
    nombre = request.form["nombre"]
    email = request.form["email"]
    fecha_ingreso = request.form["fecha_ingreso"]
    
    alumno = edit_alumno_by_id(config.session, alumno_id, nombre, email, fecha_ingreso)
    return redirect(url_for("Alumnos.get_alumnos"))

@alumno_route_blueprint.route('/borrar_alumno/<int:alumno_id>', methods=['POST'])
def delete_alumno(alumno_id):
    delete_alumno_by_id(config.session, alumno_id)
    return redirect(url_for("Alumnos.get_alumnos"))

@alumno_route_blueprint.route('/inscribir_alumno/<int:alumno_id>/', methods=['POST'])
def register_alumno(alumno_id):
    alumno = register_alumno_in_secciones(config.session, alumno_id, request.form)
    if alumno is None:
        abort(NOT_FOUND, description="Alumno no encontrado.")
    return redirect(url_for('Alumnos.view_alumno', alumno_id=alumno_id))

@alumno_route_blueprint.route('/desinscribir_alumno/<int:seccion_id>/', methods=['POST'])
def unregister_alumno(seccion_id):
    alumno_id = request.form.get("alumno_id")
    unregister_alumno_in_seccion(config.session, seccion_id, alumno_id)
    return redirect(url_for('Alumnos.view_alumno', alumno_id=alumno_id))

@alumno_route_blueprint.route('/importar_alumnos', methods=['POST'])
def load_alumnos():
    data = request.json
    if not data:
        abort(BAD_REQUEST, description="No se recibió JSON válido.")

    create_alumnos_from_json(config.session, data)
    return jsonify({"message": "Alumnos cargados correctamente"}), 201