from flask import Blueprint, request, render_template, redirect, url_for
from db.config import db as config
from db.controller.profesor_controller import get_all_profesores, crear_profesor, get_profesor_by_id, edit_profesor_by_id, delete_profesor_by_id, get_paginated_profesores

profesor_route_blueprint = Blueprint("Profesores", __name__)

@profesor_route_blueprint.route('/profesores', methods=['GET'])
@profesor_route_blueprint.route('/profesores/<int:pagina>', methods=['GET'])
def get_profesores(pagina=1):
    profesores_per_page = 2

    resultado_paginado = get_paginated_profesores(
        session=config.session,  
        page=pagina,
        per_page=profesores_per_page
    )
    
    return render_template(
        "Profesores/profesores.html",
        profesores=resultado_paginado.items,        
        pagina_actual=pagina,                      
        total_paginas=resultado_paginado.pages,    
        total_profesores=resultado_paginado.total   
    )

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

