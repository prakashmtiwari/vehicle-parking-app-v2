from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from vpa.backend.config import DevelopmentConfig
from dotenv import load_dotenv
import os
from vpa.backend.extensions import db, migrate, security, login_manager, jwt
from vpa.backend.models import User, Role
from vpa.backend.auth import auth_bp
import click

#from .commands import create_admin

load_dotenv()

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)
    api = Api(app)
    CORS(app)

    # Security requires a datastore; supply SQLAlchemyUserDatastore
    from flask_security import SQLAlchemyUserDatastore
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore)

    # Register blueprints
    app.register_blueprint(auth_bp)
#    app.register_blueprint(api_bp)


    # with app.app_context():
    #     db.create_all()

     # custom CLI command
    @app.cli.command("seed")
    def seed():
        click.echo("Starting seed...")
       # create the admin role
        admin_role = Role.query.filter_by(name='admin').first()
        click.echo(f"Admin role query result: {admin_role}")


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


        #Create the admin user
        admin_user = User.query.filter_by(username="admin").first()
        click.echo(f"Admin user query result: {admin_user}")

        if not admin_user:
            try:
                from flask_security import hash_password
                password_hash = hash_password("admin")
                admin_user = User(
                    username="admin",
                    password=password_hash,
                    fs_uniquifier="admin-001")
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

        


    # flask-login explicit loader (Flask-Security registers its own but it's fine to have explicit)
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    return app
