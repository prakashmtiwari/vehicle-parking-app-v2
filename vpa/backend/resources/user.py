from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from vpa.backend.models import User, Role
from vpa.backend.extensions import db
from vpa.backend.utils.decorators import admin_required


class UserListResource(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        users = User.query.all()
        admin_role = "admin"

        # Exclude admin users from the list
        for user in users:
            if admin_role in [role.name for role in user.roles]:
                users.remove(user)
                break

        try: 
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
        except Exception as e:
            return {"message": f"Error fetching users: {e}"}, 500



class UserResource(Resource):
    @jwt_required()
    @admin_required
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        try:
            return {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "roles": [r.name for r in user.roles],
            }, 200  
        except Exception as e:
            return {"message": f"Error fetching user: {e}"}, 500

    @jwt_required()
    @admin_required
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        user.username = data.get("username", user.username)
        user.email = data.get("email", user.email)
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        
        password = data.get("password", "")

        try: 
            if data.get("password"):
                if len(password) < 8:
                   raise ValueError("Password must be at least 8 characters")
                user.password = generate_password_hash(data["password"])

            db.session.commit()
            return {"message": "User updated"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error updating user: {e}"}, 500    

    @jwt_required()
    @admin_required
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 200
