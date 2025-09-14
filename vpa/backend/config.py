import os

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-change-me")
#    SQLALCHEMY_DATABASE_URI = os.environ.get(
#        "SQLALCHEMY_DATABASE_URI", f"sqlite:///{os.path.join(basedir, '..', '..', 'instance', 'vehicle-parking.sqlite3')}"
#    )
#    SQLALCHEMY_DATABASE_URI = 'sqlite:////home/user/22f1000252/vehicle-parking-app-v2/vpa/backend/instance/vehicle-parking.sqlite3'
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "instance", "vehicle-parking.sqlite3") 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Flask-Security-Too
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", "change-me-salt")
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False   # disable email sending by default
    SECURITY_RECOVERABLE = True
    SECURITY_TRACKABLE = True
    SECURITY_CONFIRMABLE = False  # set True if you want confirm flow with emails
    SECURITY_POST_LOGIN_VIEW = None
    SECURITY_POST_REGISTER_VIEW = None

    # JWT for API tokens
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-secret-change-me")
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get("JWT_EXPIRES_SECONDS", 3600))

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False
