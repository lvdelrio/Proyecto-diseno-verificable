from flask import Blueprint, redirect, url_for, render_template

from db.config import db
from routes.utils.notas_finales import export_notas_to_csv, export_alumno_notas_to_csv
from db.controller.evaluacion_controller import get_evaluacion_by_id
from db.controller.common_controller import get_seccion_by_id, get_notas_by_evaluacion_id, get_notas_finales_by_seccion_id
from db.controller.common_controller import get_alumno_report_data_by_alumno_id

nota_final_route_blueprint  = Blueprint("Notas_Finales", __name__)

PATH_REPORT_EVALUACION = "evaluacion"
PATH_REPORT_SECCION = "seccion"
PATH_REPORT_ALUMNO = "alumno"

@nota_final_route_blueprint.route("/notas_finales", methods=["POST"])
def add_nota_final():
    return redirect(url_for("NotasFinales.view_notas_finales",))

@nota_final_route_blueprint.route("/reporte_evaluacion/<int:evaluacion_id>", methods=["GET"])
def generate_evaluacion_report(evaluacion_id):
    evaluacion = get_evaluacion_by_id(db.session, evaluacion_id)

    notas_de_evaluacion = get_notas_by_evaluacion_id(db.session, evaluacion_id)
    nota_values = [nota.nota for nota in notas_de_evaluacion]
    export_notas_to_csv(nota_values, PATH_REPORT_EVALUACION)
    return render_template('Secciones/partials/evaluaciones/edit_evaluacion.html',
                           evaluacion=evaluacion, seccion=evaluacion.categoria.seccion)

@nota_final_route_blueprint.route("/reporte_seccion/<int:seccion_id>", methods=["GET"])
def generate_seccion_report(seccion_id):
    seccion = get_seccion_by_id(db.session, seccion_id)

    closed_seccion_notas_finales = get_notas_finales_by_seccion_id(db.session, seccion_id)
    nota_values = [nota.nota_final for nota in closed_seccion_notas_finales]
    export_notas_to_csv(nota_values, PATH_REPORT_SECCION)

    return render_template("secciones/detalle_seccion.html", seccion=seccion, tab="info")

@nota_final_route_blueprint.route("/reporte_alumno/<int:alumno_id>", methods=["GET"])
def generate_alumno_report(alumno_id):
    report_data = get_alumno_report_data_by_alumno_id(db.session, alumno_id)
    export_alumno_notas_to_csv(report_data, PATH_REPORT_ALUMNO)

    return redirect(url_for('Alumnos.view_alumno', alumno_id=alumno_id))