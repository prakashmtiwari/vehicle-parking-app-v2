from flask import Blueprint, jsonify, request
from vpa.beserver.extensions import db
from vpa.beserver.models import User, Role
from vpa.beserver.utils.email_validator import is_valid_email
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import re
import logging

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
# ------------------------
# REGISTER ENDPOINT
# ------------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}

    try:
        email = data.get("email", "")
        username = data.get("username")
        password = data.get("password")  # keep raw for validation
        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")
    except Exception as e:
        logger.exception(f"User Registration Failed; {e}")
        return jsonify({"message": f"Error processing input data: {e}"}), 400

    # basic validation
    if not username or not password:
        logger.error("Both Username and Password not provided!!")
        return jsonify({"message": "username and password are required"}), 400

    if username.lower() == "admin":
        logger.error("Tried to create user with username admin!!")
        return jsonify({"message": "username 'admin' is reserved."}), 400
    
    if User.query.filter_by(email=email).first():
        logger.error(f"User with email address: {email} exists already!!")
        return jsonify({"message": "Email already exists"}), 400

    if User.query.filter_by(username=username).first():
        logger.error(f"User with username: {username} exists already!!")
        return jsonify({"message": "Username already exists"}), 400
    
    #check if email is valid
    if email:
        if is_valid_email(email):
            logger.info(f"The Submitted Email Address '{email}' is valid")
        else:
            logger.error(f"The Submitted Email Address '{email}' is invalid")

    if len(password) < 6:
        logger.error(f"The provided password is too short!!")
        return jsonify({"message": "password too short, at least 6 characters required."}), 400

    try:
        user = User(
            email=email,
            username=username,
            password=generate_password_hash(password),
            first_name=first_name,
            last_name=last_name
       )
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Error creating user: {e}"}), 500
    
    # assign default "user" role
    try:
        user_role = Role.query.filter_by(name="user").first()
        if user_role:
            user.roles.append(user_role)
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Error assigning default role: {e}"}), 500

    return jsonify({
        "success": True,
        "message": "User registered successfully",
        "data": {"id": user.id, "username": user.username}
    }), 201


# ------------------------
# LOGIN ENDPOINT
# ------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "username and password required"}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid username or password"}), 401
        

    # collect roles
    user_roles = [role.name for role in user.roles]


    user_id = data.get("id")
    if user_id and str(user.id) != str(user_id):
        return jsonify({"message": "User ID does not match username"}), 401

    # create JWT with roles in identity
    additional_claims = {"username": user.username, "user_id":user_id ,"role": [r.name for r in user.roles]}
    access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)

    return jsonify({
        "success": True,
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "roles": user_roles
        }
    }), 200
