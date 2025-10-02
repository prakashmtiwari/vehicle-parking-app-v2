from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        roles = claims.get("role", [])

        if "admin" not in roles:
            return jsonify({"msg": "Admins only!"}), 403

        return fn(*args, **kwargs)
    return wrapper

def user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        roles = claims.get("role", [])

        if "user" not in roles:
            return jsonify({"msg": "Users only!"}), 403

        return fn(*args, **kwargs)
    return wrapper