from flask import Blueprint, request, jsonify
from models import User
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

def bad_request(msg="Invalid request"):
    return jsonify({"msg": msg}), 400

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''

    if not username or not password:
        return bad_request("username และ password ต้องไม่ว่าง")

    if User.objects(username=username).first():
        return bad_request("Username already exists")

    hashed_pw = generate_password_hash(password)
    user = User(username=username, password=hashed_pw).save()
    return jsonify({"msg": "User registered successfully"}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''

    if not username or not password:
        return bad_request("กรอก username และ password ให้ครบ")

    user = User.objects(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify(access_token=access_token), 200

@auth.route('/me', methods=['GET'])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.objects(id=user_id).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404
    return jsonify({"id": str(user.id), "username": user.username}), 200
