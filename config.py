import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = ENV == "development"

    ADMIN_KEY = os.getenv("ADMIN_KEY")

    if not ADMIN_KEY:
        raise ValueError(
            "Please specify the ADMIN_KEY environment variable.\n"
            "This is required for all mutating operations in the API."
        )

    SECRET_KEY = os.getenv("SECRET_KEY")

    if not SECRET_KEY:
        raise ValueError(
            "Please specify the SECRET_KEY environment variable.\n"
            "This is required for session management and CSRF protection."
        )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@localhost:5432/dance_db",
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
