"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Blueprint('api', __name__)
origins = ["https://super-potato-5gxr57xj6wpj3vq9p-3001.app.github.dev"]
# Allow CORS requests to this API
# CORS(api, supports_credentials=True, origins=[
#  "https://super-potato-5gxr57xj6wpj3vq9p-3000.app.github.dev"])


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


@api.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"msg": "Email and password are required"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"msg": "User already exists"}), 409
    hashed_password = generate_password_hash(password)
    new_user = User(email=email, password=hashed_password, is_active=True)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201


@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"msg": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"msg": "User not found"}), 404

    if not check_password_hash(user.password, password):
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = create_access_token(
        identity=str(user.id))  # Convertir a string
    return jsonify({"token": access_token}), 200


@api.route('/private', methods=['GET'])
@jwt_required()
def private():
    try:
        current_user_id = get_jwt_identity()

        if not str(current_user_id).isdigit():
            return jsonify({"error": "user id invalido"}), 422

        user = User.query.get(int(current_user_id))
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        return jsonify({"msg": f"Bienvenido {user.email}"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
