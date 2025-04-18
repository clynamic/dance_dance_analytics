import uuid

from slugify import slugify
from sqlalchemy import func
from app.database import db
from app.models.song_record import SongRecord
from sqlalchemy import inspect, event


class MixRecord(db.Model):
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
