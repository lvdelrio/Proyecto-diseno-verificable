from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
from dotenv import load_dotenv
from db import db, init_db, Course
import routes.userRoutes as userRoutes

# Load environment variables from .env
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5000"]}})
# Initialize the database
init_db(app)

app.add_url_rule("/add_user/<name>/<email>", "add_user", userRoutes.add_user)

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    print("Aqui tamo en el home hermano")
    return render_template("index.html")

@app.route('/cursos', methods=['GET'])
def get_cursos():
    cursos = Course.query.all()
    return render_template("Cursos/cursos.html", cursos=cursos)

@app.route('/curso/<int:curso_id>')
def view_curso(curso_id):
    curso = Course.query.get_or_404(curso_id)
    return render_template("Cursos/detalle_curso.html", curso=curso)

@app.route('/agregar_curso', methods=['POST'])
def add_curso():
    name = request.form.get("name")
    description = request.form.get("description", "")
    
    new_course = Course(name=name, description=description)
    db.session.add(new_course)
    db.session.commit()

    return redirect(url_for("get_cursos"))

@app.route('/editar_curso/<int:curso_id>', methods=['POST'])
def edit_curso(curso_id):
    curso = Course.query.get_or_404(curso_id)
    curso.name = request.form["name"]
    curso.description = request.form["description"]
    db.session.commit()
    
    return redirect(url_for("get_cursos"))

@app.route('/borrar_curso/<int:curso_id>', methods=['POST'])
def delete_curso(curso_id):
    curso = Course.query.get_or_404(curso_id)
    db.session.delete(curso)
    db.session.commit()
    return redirect(url_for("get_cursos"))

if __name__ == "__main__":
    app.run(debug=True)