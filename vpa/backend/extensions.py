from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import Security
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_restful import Api

db = SQLAlchemy()
migrate = Migrate()
security = Security()
login_manager = LoginManager()
jwt = JWTManager()
api = Api()
