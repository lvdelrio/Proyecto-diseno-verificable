import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI') #Sacar configuracion del .env
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)