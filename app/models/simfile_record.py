import uuid
import hashlib
from app.database import db
from simfile import loads as parse_simfile
from functools import cached_property


class SimfileRecord(db.Model):
    __tablename__ = "simfile_records"

    id = db.Column(db.Uuid, primary_key=True, default=uuid.uuid4)
    text = db.Column(db.Text, nullable=False)
    hash = db.Column(db.String(64), nullable=False, unique=True)

    base_info = db.relationship(
        "SongRecord", back_populates="simfile", uselist=False, cascade="all, delete"
    )
    charts = db.relationship(
        "ChartRecord", back_populates="simfile", cascade="all, delete"
    )

    @classmethod
    def from_string(cls, simfile_text: str) -> "SimfileRecord":
        hash_value = hashlib.sha256(simfile_text.encode("utf-8")).hexdigest()
        return cls(text=simfile_text, hash=hash_value)

    @cached_property
    def simfile(self):
        return parse_simfile(self.text)
