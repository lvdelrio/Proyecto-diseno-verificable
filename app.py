from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
from dotenv import load_dotenv
from db import db, init_db

from routes.cursos_routes import course_route_blueprint
from routes.profesores_routes import profesor_route_blueprint
from routes.alumno_routes import alumno_route_blueprint

# Load environment variables from .env
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)

# Add routes for api
app.register_blueprint(course_route_blueprint, url_prefix="")
app.register_blueprint(profesor_route_blueprint, url_prefix="")
app.register_blueprint(alumno_route_blueprint, url_prefix="")


CORS(app, resources={r"/*": {"origins": ["http://localhost:5000"]}})

# Initialize the database
init_db(app)

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)