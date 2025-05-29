from flask import Blueprint, request, render_template, redirect, url_for
from db.config import db as config



nota_final_route_blueprint  = Blueprint("Notas_Finales", __name__)

@nota_final_route_blueprint.route("/notas_finales", methods=["POST"])
def add_nota_final():
    return redirect(url_for("NotasFinales.view_notas_finales",))