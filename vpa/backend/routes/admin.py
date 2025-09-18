from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from vpa.backend.models import User

admin_bp = Blueprint("admin_bp", __name__, url_prefix='/admin')


def is_admin(user):
    return any(role.name == "admin" for role in user.roles)

@admin_bp.route("users", methods=["GET"])
@jwt_required()

