import uuid
from app.database import db


class MixRecord(db.Model):
    __tablename__ = "mix_records"

    id = db.Column(db.Uuid, primary_key=True, default=uuid.uuid4)
    title = db.Column(db.Text, nullable=False)
    system = db.Column(db.Text, nullable=False)
    region = db.Column(db.Text, nullable=False)
    release = db.Column(db.Date, nullable=False)

    banner_id = db.Column(
        db.Uuid, db.ForeignKey("banner_records.id"), nullable=True, unique=True
    )
    banner = db.relationship("BannerRecord", back_populates="mix", uselist=False)
