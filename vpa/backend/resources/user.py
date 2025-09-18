from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from vpa.backend.models import User, Role
from vpa.backend.extensions import db

def is_admin(user):
    return any(role.name == "admin" for role in user.roles)

class UserListResource(Resource):
    @jwt_required()
    def get(self):
        current_user = User.query.get(get_jwt_identity()["id"])
        if not current_user or not is_admin(current_user):
            return {"message": "Forbidden"}, 403

        users = User.query.all()
        return [
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "fullname": f"{u.first_name or ''} {u.last_name or ''}".strip(),
                "roles": [r.name for r in u.roles],
            }
            for u in users
        ], 200

    @jwt_required()
    def post(self):
        current_user = User.query.get(get_jwt_identity()["id"])
        if not current_user or not is_admin(current_user):
            return {"message": "Forbidden"}, 403

        data = request.get_json()
        if not data.get("username") or not data.get("password"):
            return {"message": "username and password required"}, 400
        
        try:
            new_user = User(
                username=data["username"],
                email=data.get("email"),
                password=generate_password_hash(data["password"]),
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
            )
        except Exception as e:
            return {"message": f"Error creating user: {e}"}, 400

        # Add default "user" role
        try:
            user_role = Role.query.filter_by(name="user").first()
            if user_role:
                new_user.roles.append(user_role)
        except Exception as e:
            return {"message": f"Error assigning default role: {e}"}, 400        


        db.session.add(new_user)
        db.session.commit()
        return {"message": "User created", "id": new_user.id}, 201


class UserResource(Resource):
    @jwt_required()
    def put(self, user_id):
        current_user = User.query.get(get_jwt_identity()["id"])
        if not current_user or not is_admin(current_user):
            return {"message": "Forbidden"}, 403

        user = User.query.get_or_404(user_id)
        data = request.get_json()
        user.username = data.get("username", user.username)
        user.email = data.get("email", user.email)
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        if data.get("password"):
            user.password = generate_password_hash(data["password"])

        db.session.commit()
        return {"message": "User updated"}, 200

    @jwt_required()
    def delete(self, user_id):
        current_user = User.query.get(get_jwt_identity()["id"])
        if not current_user or not is_admin(current_user):
            return {"message": "Forbidden"}, 403

        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 200
