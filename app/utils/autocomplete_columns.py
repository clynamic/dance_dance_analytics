from app.database import db


class AutocompleteMixin:
    @classmethod
    def _distinct_column_values(cls, column, query=None, limit=10):
        q = db.session.query(column).distinct().order_by(column)
        if query:
            q = q.filter(column.ilike(f"%{query}%"))
        q = q.limit(limit)
        return [r[0] for r in q.all() if r[0]]

    @classmethod
    def get_autocomplete(cls, column_name, query=None, limit=10):
        column = getattr(cls, column_name)
        return cls._distinct_column_values(column, query=query, limit=limit)
