import os
from dotenv import load_dotenv

# Load .env at the top of config.py
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    # Secret and runtime settings
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")
    DEBUG = os.environ.get("FLASK_DEBUG", "False").lower() in ("1", "true", "yes", "on")
    APP_HOST = os.environ.get("APP_HOST", "0.0.0.0")
    APP_PORT = int(os.environ.get("APP_PORT", "5000"))
    APP_BASE_URL = os.environ.get(
        "APP_BASE_URL", f"http://localhost:{os.environ.get('APP_PORT', '5000')}"
    )

    # PostgreSQL database configuration
    DATABASE_URL = os.environ.get("DATABASE_URL")
    DB_USER = os.environ.get("DB_USER", "postgres")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "123456")
    DB_HOST = os.environ.get("DB_HOST", "postgres")
    DB_PORT = os.environ.get("DB_PORT", "5432")
    DB_NAME = os.environ.get("DB_NAME", "parking-db")
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    print(f"Using database URI: {SQLALCHEMY_DATABASE_URI}")
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
    CACHE_REDIS_HOST = os.environ.get("CACHE_REDIS_HOST", "redis")
    CACHE_REDIS_PORT = int(os.environ.get("CACHE_REDIS_PORT", 6379))
    CACHE_REDIS_DB = int(os.environ.get("CACHE_REDIS_DB", 0))
    CACHE_REDIS_URL = os.environ.get("CACHE_REDIS_URL", "redis://redis:6379/0")
    CACHE_REDIS_PASSWORD = os.environ.get("CACHE_REDIS_PASSWORD", None)
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get("CACHE_DEFAULT_TIMEOUT", 300))
    
    # Export settings
    EXPORT_DIR = os.environ.get("EXPORT_DIR", "exports")
    EXPORT_DOWNLOAD_BASE_URL = os.environ.get("EXPORT_DOWNLOAD_BASE_URL", APP_BASE_URL)

    # Email settings
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "localhost")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 25))
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "noreply@example.com")

    # Celery backend and broker
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://@redis:6379/1")
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://@redis:6379/2")

    REMINDER_CRON = os.environ.get("REMINDER_CRON", "50 14 * * *")


    # G-chat webhook url
    GOOGLE_CHAT_WEBHOOK_URL = os.environ.get("GOOGLE_CHAT_WEBHOOK_URL", None)

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False
