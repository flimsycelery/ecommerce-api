import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY=os.getenv("SECRET_KEY","dev-secret-change-this")
    JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY","dev-jwt-secret-change-this")
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)

class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI="sqlite:///ecommerce.db"

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_ACCESS_TOKEN_EXPIRES = 60

class ProductionConfig(Config):
    DEBUG = False
    _db_url = os.getenv("DATABASE_URL", "")
    SQLALCHEMY_DATABASE_URI=_db_url.replace("postgresql://", "postgresql+psycopg2://") if _db_url else ""

config_map = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}

def get_config():
    env=os.getenv("FLASK_ENV","development")
    return config_map.get(env,DevelopmentConfig)