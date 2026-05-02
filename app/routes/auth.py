from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError
from app.extensions import db, limiter
from app.models.user import User
from app.schemas import RegisterSchema, LoginSchema

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    schema = RegisterSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.messages}), 422

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 409

    user = User(name=data["name"], email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully", "user": user.to_dict()}), 201


@auth_bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    schema = LoginSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.messages}), 422

    user = User.query.filter_by(email=data["email"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid email or password"}), 401

    token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )
    return jsonify({"access_token": token, "user": user.to_dict()}), 200