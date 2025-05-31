from app.database import db
from sqlalchemy.inspection import inspect
from sqlalchemy import inspect, or_
import uuid

from app.utils.query_builder import build_dynamic_query


class BaseModel(db.Model):
    __abstract__ = True

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    @classmethod
    def get(cls, identifier):
        uuid_obj = None
        try:
            uuid_obj = uuid.UUID(identifier)
        except (ValueError, TypeError):
            pass

        filters = []
        if uuid_obj:
            filters.append(cls.id == uuid_obj)
        if hasattr(cls, "slug"):
            filters.append(cls.slug == identifier)

        if not filters:
            return None

        return cls.query.filter(or_(*filters)).first()

    @classmethod
    def query_with_filters(cls, query_params, custom_fields=None, extra_fields=None):
        fields = custom_fields or getattr(cls, "QUERY_FIELDS", {})
        if extra_fields:
            fields = {**fields, **extra_fields}

        query = cls.query
        return build_dynamic_query(query, query_params, fields)
