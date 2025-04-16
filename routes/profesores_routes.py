from flask import Blueprint, request, render_template, redirect, url_for, abort
from db.config import db as config
from db.controller.curso_controller import get_all_cursos
from db.controller.seccion_controller import get_all_secciones_by_curso_id
from db.controller.profesor_controller import (
    get_all_profesores, 
    create_profesor, 
    get_profesor_by_id, 
    edit_profesor_by_id, 
    delete_profesor_by_id, 
    get_paginated_profesores, 
    enroll_profesor_in_seccion 
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
    profesor = get_profesor_by_id(config.session, profesor_id)
    if profesor is None:
        abort(404, description="Profesor no encontrado.")

    profesor_seccion_ids = {seccion.id for seccion in profesor.secciones}

    cursos_con_secciones = []
    for curso in get_all_cursos(config.session):
        secciones_disponibles = [
            seccion for seccion in get_all_secciones_by_curso_id(config.session, curso.id)
            if seccion.id not in profesor_seccion_ids
        ]

        if secciones_disponibles:
            cursos_con_secciones.append((curso, secciones_disponibles))

    return render_template(
        "Profesores/detalle_profesor.html",
        profesor=profesor,
        cursos_con_secciones=cursos_con_secciones
    )

@profesor_route_blueprint.route('/agregar_profesor', methods=['POST'])
def add_profesor():
    nombre = request.form.get("nombre")
    email = request.form.get("email", "")
    print(nombre, email)
    profesor = create_profesor(config.session, nombre, email)

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

@profesor_route_blueprint.route('/inscribir/<int:profesor_id>/', methods=['POST'])
def inscribir_profesor(profesor_id):
    profesor = get_profesor_by_id(config.session, profesor_id)

    seccion_ids = request.form.getlist("seccion_ids")
    print("Secciones seleccionadas:", seccion_ids)

    enrolled_sections = []
    errors = []

    for seccion_id in seccion_ids:
        exito, mensaje = enroll_profesor_in_seccion(config.session, profesor_id, int(seccion_id))
        if exito:
            enrolled_sections.append(mensaje)
        else:
            errors.append(mensaje)

    return redirect(url_for('Profesores.view_profesor', profesor_id=profesor_id))
