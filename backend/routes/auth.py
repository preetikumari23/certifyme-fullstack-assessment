from flask import Blueprint, request, jsonify, session
from models import db, Admin
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json

    if Admin.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Account already exists"}), 400

    if data['password'] != data['confirm_password']:
        return jsonify({"error": "Passwords do not match"}), 400

    if len(data['password']) < 8:
        return jsonify({"error": "Password too short"}), 400

    admin = Admin(
        full_name=data['full_name'],
        email=data['email'],
        password=generate_password_hash(data['password'])
    )

    db.session.add(admin)
    db.session.commit()

    return jsonify({"message": "Signup successful"})


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json

    admin = Admin.query.filter_by(email=data['email']).first()

    if not admin or not check_password_hash(admin.password, data['password']):
        return jsonify({"error": "Invalid email or password"}), 401

    session['admin_id'] = admin.id
    session.permanent = True

    return jsonify({"message": "Login successful"})