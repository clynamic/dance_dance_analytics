import uuid
from app.database import db


class BannerRecord(db.Model):
    __tablename__ = "banner_records"

    id = db.Column(db.Uuid, primary_key=True, default=uuid.uuid4)
    blob = db.Column(db.LargeBinary, nullable=False)

    mix = db.relationship("MixRecord", back_populates="banner", uselist=False)
    song = db.relationship("SongRecord", back_populates="banner", uselist=False)
