from flask import Blueprint, request, render_template, redirect, url_for, flash, abort, jsonify
from flask import Blueprint, request, render_template, redirect, url_for, flash, abort, jsonify
from db.config import db as config
from db.controller.curso_controller import get_all_cursos
from db.controller.seccion_controller import get_all_secciones_by_curso_id
from db.controller.alumno_controller import (
    get_all_alumnos,
    create_alumno,
    get_alumno_by_id,
    edit_alumno_by_id,
    delete_alumno_by_id,
    get_paginated_alumnos,
    enroll_alumno_in_seccion,
    create_alumno_seccion_from_json,
    create_alumnos_from_json
)

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
    alumno = get_alumno_by_id(config.session, alumno_id)

    if alumno is None:
        abort(404, description="Alumno no encontrado.")

    registered_cursos_ids = {seccion.curso_id for seccion in alumno.secciones}

    available_cursos = [
        curso for curso in get_all_cursos(config.session)
        if curso.id not in registered_cursos_ids
    ]

    cursos_with_secciones = []
    for curso in available_cursos:
        secciones = get_all_secciones_by_curso_id(config.session, curso.id)
        if(len(secciones)==0): continue
        cursos_with_secciones.append((curso, secciones))

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
    alumno = get_alumno_by_id(config.session, alumno_id)
    cursos = get_all_cursos(config.session)

    enrolled_sections = []
    errors = []

    for curso in cursos:
        seccion_id = request.form.get(f'seccion_id_{curso.id}')
        if seccion_id:
            exito, mensaje = enroll_alumno_in_seccion(config.session, alumno_id, int(seccion_id))
            if exito:
                enrolled_sections.append(mensaje)
            else:
                errors.append(mensaje)

    return redirect(url_for('Alumnos.view_alumno', alumno_id=alumno_id))

@alumno_route_blueprint.route('/importar_alumnos_seccion', methods=['POST'])
def load_alumnos_seccion():
    data = request.json
    if not data:
        abort(400, description="No se recibió JSON válido.")

    create_alumno_seccion_from_json(config.session, data)
    return jsonify({"message": "Alumnos cargados correctamente"}), 201


@alumno_route_blueprint.route('/importar_alumnos', methods=['POST'])
def load_alumnos():
    data = request.json
    if not data:
        abort(400, description="No se recibió JSON válido.")

    create_alumnos_from_json(config.session, data)
    return jsonify({"message": "Alumnos cargados correctamente"}), 201