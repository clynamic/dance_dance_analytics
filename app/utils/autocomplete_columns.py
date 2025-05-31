from app.database import db


class AutocompleteMixin:
    @classmethod
    def _distinct_column_values(cls, column):
        results = db.session.query(column).distinct().order_by(column).all()
        return [r[0] for r in results if r[0]]

    @classmethod
    def get_autocomplete(cls, column_name):
        column = getattr(cls, column_name)
        return cls._distinct_column_values(column)
