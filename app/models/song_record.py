from app.database import db
from slugify import slugify
from simfile.types import Simfile
from sqlalchemy import inspect, event

from app.models.chart_record import ChartRecord
from app.utils.autocomplete_columns import AutocompleteMixin
from app.utils.base_model import BaseModel


class SongRecord(BaseModel, AutocompleteMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    __tablename__ = "song_records"

    id = db.Column(db.Uuid, db.ForeignKey("simfile_records.id"), primary_key=True)
    simfile = db.relationship("SimfileRecord", back_populates="song", uselist=False)

    mix_id = db.Column(db.Uuid, db.ForeignKey("mix_records.id"), nullable=False)
    mix = db.relationship("MixRecord", back_populates="songs")

    banner_id = db.Column(
        db.Uuid, db.ForeignKey("banner_records.id"), nullable=True, unique=True
    )
    banner = db.relationship("BannerRecord", back_populates="song", uselist=False)

    title = db.Column(db.Text, nullable=True)
    slug = db.Column(db.Text, nullable=False)
    artist = db.Column(db.Text, nullable=True)
    title_translit = db.Column(db.Text, nullable=True)
    artist_translit = db.Column(db.Text, nullable=True)

    samplestart = db.Column(db.Float, nullable=True)
    samplelength = db.Column(db.Float, nullable=True)
    displaybpm = db.Column(db.Text, nullable=True)
    stops = db.Column(db.Text, nullable=True)
    bpms = db.Column(db.Text, nullable=True)

    charts = db.relationship(
        "ChartRecord", back_populates="song", cascade="all, delete"
    )

    QUERY_FIELDS = {
        "id": ("id", [id, slug]),
        "title": ("text", title),
        "title_translit": ("text", title_translit),
        "artist": ("text", artist),
        "artist_translit": ("text", artist_translit),
    }

    @classmethod
    def by_slug(cls, mix_slug: str, song_slug: str):
        from app.models.mix_record import MixRecord

        return (
            db.session.query(cls)
            .join(MixRecord)
            .filter(MixRecord.slug == mix_slug, cls.slug == song_slug)
            .one_or_none()
        )

    @classmethod
    def get(cls, id=None, mix_slug=None, song_slug=None):
        if mix_slug and song_slug:
            return cls.by_slug(mix_slug, song_slug)
        elif id:
            return cls.by_id(id)
        else:
            raise ValueError("Either id or (mix_slug, song_slug) must be provided.")

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
            charts=[ChartRecord.from_sim(chart) for chart in sim.charts],
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
