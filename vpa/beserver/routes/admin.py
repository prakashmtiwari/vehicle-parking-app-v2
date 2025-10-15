from flask import Blueprint, jsonify
from vpa.beserver.models import User

admin_bp = Blueprint("admin_bp", __name__, url_prefix='/admin')


def is_admin(user):
    return any(role.name == "admin" for role in user.roles)


