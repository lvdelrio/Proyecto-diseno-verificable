from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from db import db, init_db, Course

# Load environment variables from .env
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5000"]}})

# Initialize the database
init_db(app)

#iniciar base de datos a  lo maldito
@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/cursos', methods=['GET'])
def get_cursos():
    cursos = Course.query.all()
    return render_template("cursos.html", cursos=cursos)

@app.route('/agregar_curso', methods=['POST'])
def add_curso():
    name = request.form.get("name")
    description = request.form.get("description", "")
    
    new_course = Course(name=name, description=description)
    db.session.add(new_course)
    db.session.commit()

    return redirect(url_for("get_cursos"))

@app.route('/borrar_curso/<int:curso_id>', methods=['DELETE'])
def delete_curso(curso_id):
    curso = Course.query.get_or_404(curso_id)
    db.session.delete(curso)
    db.session.commit()
    return jsonify({"message": "Curso deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)