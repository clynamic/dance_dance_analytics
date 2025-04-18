from app.database import db
from slugify import slugify
from simfile import Simfile
from sqlalchemy import inspect, event


class SongRecord(db.Model):
    __tablename__ = "song_records"

    id = db.Column(db.Uuid, db.ForeignKey("simfile_records.id"), primary_key=True)
    simfile = db.relationship("SimfileRecord", back_populates="song", uselist=False)

    mix_id = db.Column(db.Uuid, db.ForeignKey("mix_records.id"), nullable=False)
    mix = db.relationship("MixRecord", back_populates="songs")

    title = db.Column(db.Text, nullable=True)
    slug = db.Column(db.Text, nullable=False, unique=True)
    artist = db.Column(db.Text, nullable=True)
    title_translit = db.Column(db.Text, nullable=True)
    artist_translit = db.Column(db.Text, nullable=True)

    samplestart = db.Column(db.Float, nullable=True)
    samplelength = db.Column(db.Float, nullable=True)
    displaybpm = db.Column(db.Text, nullable=True)

    stops = db.Column(db.Text, nullable=True)
    bpms = db.Column(db.Text, nullable=True)

    @classmethod
    def from_sim(cls, sim: Simfile) -> "SongRecord":
        return cls(
            title=sim.title,
            artist=sim.artist,
            title_translit=sim.titletranslit,
            artist_translit=sim.artisttranslit,
            samplestart=cls._safe_float(sim.samplestart),
            samplelength=cls._safe_float(sim.samplelength),
            displaybpm=sim.displaybpm,
            stops=str(sim.stops) if sim.stops else None,
            bpms=str(sim.bpms) if sim.bpms else None,
        )

    @staticmethod
    def _safe_float(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return None


@event.listens_for(SongRecord, "before_insert")
def on_insert(mapper, conn, target):
    target.slug = slugify(target.title)


@event.listens_for(SongRecord, "before_update")
def on_update(mapper, conn, target):
    if inspect(target).attrs.title.history.has_changes():
        target.slug = slugify(target.title)
