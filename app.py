from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
from dotenv import load_dotenv
from db.config import db as config
from db import db, init_db

from routes.cursos_routes import curso_route_blueprint
from routes.profesores_routes import profesor_route_blueprint
from routes.alumnos_routes import alumno_route_blueprint
from routes.notas_finales_routes import nota_final_route_blueprint
from routes.secciones_routes import seccion_route_blueprint
from routes.evaluacion_routes import evaluacion_blueprint
from routes.categoria_routes import categoria_blueprint

load_dotenv()

app = Flask(__name__)

app.register_blueprint(curso_route_blueprint, url_prefix="")
app.register_blueprint(profesor_route_blueprint, url_prefix="")
app.register_blueprint(alumno_route_blueprint, url_prefix="")
app.register_blueprint(nota_final_route_blueprint, url_prefix="")
app.register_blueprint(seccion_route_blueprint, url_prefix="")
app.register_blueprint(evaluacion_blueprint, url_prefix="")
app.register_blueprint(categoria_blueprint, url_prefix="")

CORS(app, resources={r"/*": {"origins": ["http://localhost:5000"]}})

init_db(app)

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/testing', methods = ['GET'])
def testing():
    from db.test_sql import test_sql
    test_sql()
    return "Testing"


if __name__ == "__main__":
    app.run(debug=True)