import uuid

from slugify import slugify
from sqlalchemy import func
from app.database import db
from app.models.song_record import SongRecord
from sqlalchemy import inspect, event

from app.utils.autocomplete_columns import AutocompleteMixin
from app.utils.base_model import BaseModel


class MixRecord(BaseModel, AutocompleteMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    __tablename__ = "mix_records"

    id = db.Column(db.Uuid, primary_key=True, default=uuid.uuid4)
    title = db.Column(db.Text, nullable=False)
    slug = db.Column(db.Text, nullable=False, unique=True)
    system = db.Column(db.Text, nullable=False)
    region = db.Column(db.Text, nullable=False)
    release = db.Column(db.Date, nullable=False)

    banner_id = db.Column(
        db.Uuid, db.ForeignKey("banner_records.id"), nullable=True, unique=True
    )
    banner = db.relationship("BannerRecord", back_populates="mix", uselist=False)

    songs = db.relationship("SongRecord", back_populates="mix", cascade="all, delete")

    QUERY_FIELDS = {
        "id": ("id", [id, slug]),
        "title": ("text", title),
        "system": ("text", system),
        "region": ("text", region),
        "release": ("date", release),
    }

    @classmethod
    def by_slug(cls, slug: str):
        return db.session.query(cls).filter_by(slug=slug).one_or_none()

    @classmethod
    def get(cls, slug=None, id=None):
        if slug:
            return cls.by_slug(slug)
        elif id:
            return cls.by_id(id)
        else:
            raise ValueError("Either slug or id must be provided.")

    @property
    def song_count(self) -> int:
        return (
            db.session.query(func.count(SongRecord.id))
            .filter_by(mix_id=self.id)
            .scalar()
        )


@event.listens_for(MixRecord, "before_insert")
def on_insert(mapper, conn, target):
    target.slug = slugify(target.title)


@event.listens_for(MixRecord, "before_update")
def on_update(mapper, conn, target):
    if inspect(target).attrs.title.history.has_changes():
        target.slug = slugify(target.title)
