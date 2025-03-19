from flask import Flask
from dotenv import load_dotenv
from db import db, init_db, Course

# Load environment variables from .env
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)

# Initialize the database
init_db(app)

#iniciar base de datos a  lo maldito
@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return "Welcome to the Course Organizer!"

# Route to add a course
@app.route('/add_course/<name>/<description>', methods=['GET'])
def add_course(name, description):
    new_course = Course(name=name, description=description)
    db.session.add(new_course)
    db.session.commit()
    return f"Added course: {name}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)