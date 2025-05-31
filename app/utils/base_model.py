from app.database import db
from sqlalchemy.inspection import inspect


class BaseModel(db.Model):
    __abstract__ = True

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
