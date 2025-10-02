from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from vpa.beserver.models import User, Role
from vpa.beserver.extensions import db

class CurrentUserResource(Resource):
    @jwt_required()
    def get(self):
        """Get current logged-in user's details"""
        user = User.query.get_or_404(get_jwt_identity()["id"])
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "roles": [r.name for r in user.roles],
        }, 200

    @jwt_required()
    def put(self):
        """Update current user's profile"""
        user = User.query.get_or_404(get_jwt_identity()["id"])
        data = request.get_json() or {}

        if "email" in data:
            user.email = data["email"]
        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]
        if "password" in data:  # allow password change
            user.password = generate_password_hash(data["password"])

        db.session.commit()
        return {"message": "Profile updated successfully"}, 200
