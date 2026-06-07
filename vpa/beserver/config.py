import os
from dotenv import load_dotenv

# Load .env at the top of config.py
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-change-me")
#    SQLALCHEMY_DATABASE_URI = os.environ.get(
#        "SQLALCHEMY_DATABASE_URI", f"sqlite:///{os.path.join(basedir, '..', '..', 'instance', 'vehicle-parking.sqlite3')}"
#    )
#    SQLALCHEMY_DATABASE_URI = 'sqlite:////home/user/22f1000252/vehicle-parking-app-v2/vpa/backend/instance/vehicle-parking.sqlite3'
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "instance", "vehicle-parking.sqlite3") 
    print (f"Using database URI: {SQLALCHEMY_DATABASE_URI}")
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
    SECURITY_POST_LOGIN_VIEW = "/post-login"

    # JWT for API tokens
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-secret-change-me")
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get("JWT_EXPIRES_SECONDS", 3600))

    # Redis Cache
    CACHE_TYPE = os.environ.get("CACHE_TYPE", "RedisCache")
    CACHE_REDIS_HOST = os.environ.get("CACHE_REDIS_HOST", "localhost")
    CACHE_REDIS_PORT = int(os.environ.get("CACHE_REDIS_PORT", 6379))
    CACHE_REDIS_DB = int(os.environ.get("CACHE_REDIS_DB", 0))
    CACHE_REDIS_URL = os.environ.get("CACHE_REDIS_URL", "redis://localhost:6379/0")
    CACHE_REDIS_PASSWORD = os.environ.get("CACHE_REDIS_PASSWORD", None)
    CACHE_DEFAULT_TIMEOUT = os.environ.get("CACHE_DEFAULT_TIMEOUT", 300)
   
    # Celery backend and broker
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://:123456@localhost:6379/1")
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://:123456@localhost:6379/2")

    REMINDER_CRON = os.environ.get("REMINDER_CRON", "50 14 * * *")


    # G-chat webhook url
    GOOGLE_CHAT_WEBHOOK_URL = os.environ.get("GOOGLE_CHAT_WEBHOOK_URL", None)

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False
