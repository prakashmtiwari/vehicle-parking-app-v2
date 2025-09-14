from flask import Blueprint, jsonify, request
from flask_security import hash_password, login_user, logout_user, current_user
from .extensions import db
from .models import User, Role
from flask_security.utils import verify_password
from flask_jwt_extended import create_access_token
from flask_login import login_required


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("register", methods=["POST"])
def register():
    data = request.get_json() or {}

# check for existing username, email, fs_uniquifier
    if User.query.filter_by(username=data.get("username")).first():
        return jsonify({"message": "Username already exists"}), 400
    
    if User.query.filter_by(email=data.get("email")).first():
        return jsonify({"message": "Email already exists"}), 400
    
    if User.query.filter_by(fs_uniquifier=data.get("fs_uniquifier")).first():
        return jsonify({"message": "fs_uniquifier already exists"}), 400

# extract and validate fields
    try:
        email = data.get("email", "")
        username = data.get("username")
        password = hash_password(data.get("password"))
        active = data.get("active", True)
        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")
        fs_uniquifier = data.get("fs_uniquifier")
    except Exception as e:
        return jsonify({"msg": f"Error processing input data: {e}"}), 400    

# basic validation
    if not username or not password or not fs_uniquifier:
        return jsonify({"msg": "email,password and fs_uniquifier required"}), 400
        
# Check password length        
    if len(password) < 6:
        return jsonify({"msg": "password too short, at least 6 character required."}), 400

    try:
        user = User(
            email=email,
            username=username,
            password=hash_password(password),
            active=active,
            first_name=first_name,
            last_name=last_name,
            fs_uniquifier=fs_uniquifier)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Error creating user: {e}"}), 500    

    return jsonify({"message": "User registered successfully"}), 201






