from app.database import db
from sqlalchemy.inspection import inspect
from sqlalchemy import inspect

from app.utils.query_builder import build_dynamic_query


class BaseModel(db.Model):
    __abstract__ = True

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    @classmethod
    def by_id(cls, id):
        return db.session.query(cls).filter_by(id=id).one_or_none()

    @classmethod
    def query_with_filters(cls, query_params, custom_fields=None, extra_fields=None):
        fields = custom_fields or getattr(cls, "QUERY_FIELDS", {})
        if extra_fields:
            fields = {**fields, **extra_fields}

        query = cls.query
        return build_dynamic_query(query, query_params, fields)
