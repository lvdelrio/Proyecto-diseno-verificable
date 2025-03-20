from flask import jsonify
from db.config import db as config
from db.controller.userController import create_user, get_user_by_id, get_all_users

def list_users():
    users = get_all_users(config.session)
    return jsonify([{"id": u.id, "name": u.name, "email": u.email} for u in users])

def add_user(name, email):
    new_user = create_user(config.session, name, email)
    return f"Added user: {new_user.name}"