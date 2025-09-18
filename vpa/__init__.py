from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from vpa.backend.config import DevelopmentConfig
from dotenv import load_dotenv
import os
from vpa.backend.extensions import db, migrate,jwt
from vpa.backend.models import User, Role
from vpa.backend.routes.auth import auth_bp
from vpa.backend.api_routes import register_resources

import click
from werkzeug.security import generate_password_hash

#from .commands import create_admin

load_dotenv()

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    api = Api(app)
    CORS(app)


    # Register blueprints
    app.register_blueprint(auth_bp)

    # Register RESTful resources
    register_resources(api)
 
    # with app.app_context():
    #     db.create_all()

     # custom CLI command
    @app.cli.command("seed")
    def seed():
        click.echo("Starting seed...")
       # create the admin and user roles
        admin_role = Role.query.filter_by(name='admin').first()
        click.echo(f"Admin role query result: {admin_role}")
        user_role = Role.query.filter_by(name='user').first()
        click.echo(f"User role query result: {user_role}")


        if not admin_role:
            try:
                admin_role = Role(name='admin', description='Superuser role; meant for a single admin user;created automatically')
                db.session.add(admin_role)
                db.session.commit()
                click.echo("Added admin role")
            except Exception as e:
                db.session.rollback()
                click.echo(f"Error creating admin role: {e}")
        else:
            click.echo("Admin role already exists.")

        if not user_role:
            try:
                user_role = Role(name='user', description='Default role for regular users')
                db.session.add(user_role)
                db.session.commit()
                click.echo("Added user role")
            except Exception as e:
                db.session.rollback()
                click.echo(f"Error creating user role: {e}")
        else:
            click.echo("User role already exists.")      


        #Create the admin user
        admin_user = User.query.filter_by(username="admin").first()
        click.echo(f"Admin user query result: {admin_user}")

        if not admin_user:
            try:
                password_hash = generate_password_hash("admin")
                admin_user = User(
                    username="admin",
                    password=password_hash,
                    )
                db.session.add(admin_user)
                db.session.commit()
                click.echo("Added admin user")
            except Exception as e:
                db.session.rollback()
                click.echo(f"Error creating admin user: {e}")
        else:       
            click.echo("Admin user already exists.")    
            # assign the admin role to the admin user
 
        if admin_role not in admin_user.roles:
            try: 
                admin_user.roles.append(admin_role)
                db.session.commit() 
                click.echo("Appended admin role to admin user")
                click.echo("Database seeded with roles and admin user.")
            except Exception as e:
                db.session.rollback()
                click.echo(f"Error assigning admin role to admin user: {e}")
        else:
            click.echo("Admin user already has admin role.")   



    return app
