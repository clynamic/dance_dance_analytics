from flask_sqlalchemy import SQLAlchemy
from flask_migrate import upgrade
from sqlalchemy.exc import OperationalError
import time

db = SQLAlchemy()


def initialize_database(app, retries=10, delay=5):
    from app import models

    with app.app_context():
        for attempt in range(retries):
            try:
                upgrade()
                print("Database upgraded successfully!")
                break
            except OperationalError as e:
                print(
                    f"Database not ready (attempt {attempt + 1}/{retries}), retrying in {delay}s..."
                )
                time.sleep(delay)
        else:
            raise RuntimeError(
                f"Database initialization failed after {retries} attempts."
            )
