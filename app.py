from flask import Flask, render_template, request, jsonify, current_app
from flask_cors import CORS
from dotenv import load_dotenv
from db.config import db as config
from db import db, init_db
from db.seeds import seed_database
from db.db_events import register_events
from db.test import reset_database
from db.db_error_handler import setup_global_error_handler

from routes.cursos_routes import curso_route_blueprint
from routes.profesores_routes import profesor_route_blueprint
from routes.alumnos_routes import alumno_route_blueprint
from routes.notas_finales_routes import nota_final_route_blueprint
from routes.secciones_routes import seccion_route_blueprint
from routes.evaluacion_routes import evaluacion_blueprint
from routes.categoria_routes import categoria_blueprint
from routes.tipo_cursos_routes import tipo_curso_route_blueprint
from routes.salas_routes import sala_route_blueprint
from routes.notas_routes import nota_route_blueprint
from routes.horario_routes import horario_route_blueprint

load_dotenv()

DEBUG_ACCEPTANCE = 'true'

app = Flask(__name__)

app.register_blueprint(curso_route_blueprint, url_prefix="")
app.register_blueprint(profesor_route_blueprint, url_prefix="")
app.register_blueprint(alumno_route_blueprint, url_prefix="")
app.register_blueprint(nota_final_route_blueprint, url_prefix="")
app.register_blueprint(seccion_route_blueprint, url_prefix="")
app.register_blueprint(evaluacion_blueprint, url_prefix="")
app.register_blueprint(categoria_blueprint, url_prefix="")
app.register_blueprint(tipo_curso_route_blueprint, url_prefix="")
app.register_blueprint(sala_route_blueprint, url_prefix="")
app.register_blueprint(nota_route_blueprint, url_prefix="")
app.register_blueprint(horario_route_blueprint, url_prefix="")

CORS(app, resources={r"/*": {"origins": ["http://localhost:5000"]}})
setup_global_error_handler(app)

init_db(app)
with app.app_context():
    register_events()

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/testing', methods = ['GET'])
def testing():
    seed_database()
    return "Testing, no ejecutar mas de una vez, creara todo dos veces"

@app.route('/reset_db', methods=['GET','POST'])
def empty_db():
    if not current_app.config.get("DEBUG", False):
        return jsonify({"error": "No permitido fuera de debug mode."}), 403

    confirm = request.args.get('confirm')
    if confirm != DEBUG_ACCEPTANCE:
        return jsonify({"advertencia": "Agregar '?confirm=true' para confirmar la limpieza."}), 400

    session = config.session
    result = reset_database(session)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
