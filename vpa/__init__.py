from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_login import LoginManager
from vpa.routes.api_routes import register_api_routes


app = Flask(__name__)


app.secret_key = '8dbd092a7ebe1e081c1f9ae70b45602d5f22a09b08d352c9bb25c13c9cc817e0'  


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicle-parking.sqlite3'

db = SQLAlchemy(app)

api = Api(app)

# Register API routes dynamically
register_api_routes(api)

# Initialize the LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

import vpa.vpa_routes
import vpa.models
