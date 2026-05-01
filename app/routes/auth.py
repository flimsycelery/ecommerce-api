from flask import Blueprint,request,jsonify
from flask_jwt_extended import create_access_token
from app.extensions import db
from app.models.user import User

auth_bp=Blueprint("auth",__name__)

@auth_bp.route("/register",methods=["POST"])
def register():
    data=request.get_json()
    if not data or not all(k in data for k in ("name","email","password")):
        return jsonify({"error": "Name, email and password are required"}),422
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}),409
    user=User(name=data["name"],email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    return jsonify({"message":"User created successfully","user":user.to_dict()}),201

@auth_bp.route("/login",methods=["POST"])
def login():
    data=request.get_json()
    if not data or not all(k in data for k in ("email","password")):
        return jsonify({"error": "Email and password are required"}),422
    
    user=User.query.filter_by(email=data["email"]).first()

    if not user or not user.check_password(data["password"]):
        return jsonify({"error":"Invalid email or password"}),401
    
    token=create_access_token(
        identity=str(user.id),
        additional_claims={"role":user.role}
    )

    return jsonify({
        "access_token":token,
        "user":user.to_dict()
    }),200

@auth_bp.route("/make-admin", methods=["POST"])
def make_admin():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    user.role = "admin"
    db.session.commit()
    return jsonify({"message": "Done", "user": user.to_dict()}), 200