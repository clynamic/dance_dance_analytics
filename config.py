import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Flask environment
    ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = ENV == "development"

    # Security
    SECRET_KEY = os.getenv("SECRET_KEY")
    ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
