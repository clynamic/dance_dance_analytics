import uuid
from app.database import db
from simfile.base import BaseChart

from app.utils.autocomplete_columns import AutocompleteMixin
from app.utils.base_model import BaseModel

from sqlalchemy import event, inspect
from slugify import slugify


class ChartRecord(BaseModel, AutocompleteMixin):
    __tablename__ = "chart_records"

    id = db.Column(db.Uuid, primary_key=True, default=uuid.uuid4)
    slug = db.Column(db.Text, nullable=False)
    song_id = db.Column(db.Uuid, db.ForeignKey("song_records.id"), nullable=False)
    song = db.relationship("SongRecord", back_populates="charts")

    single_chart = db.relationship(
        "SingleChartRecord",
        back_populates="chart",
        uselist=False,
        cascade="all, delete",
    )

    stepstype = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    difficulty = db.Column(db.Text)
    rating = db.Column(db.Integer)

    QUERY_FIELDS = {
        "id": ("id", [id, slug]),
        "stepstype": ("text", stepstype),
        "description": ("text", description),
        "difficulty": ("text", difficulty),
        "rating": ("int", rating),
        "slug": ("text", slug),
    }

    @classmethod
    def by_slug(cls, mix_slug: str, song_slug: str, chart_slug: str):
        from app.models.mix_record import MixRecord
        from app.models.song_record import SongRecord

        return (
            db.session.query(cls)
            .join(SongRecord)
            .join(SongRecord.mix)
            .filter(
                SongRecord.slug == song_slug,
                SongRecord.mix.has(MixRecord.slug == mix_slug),
                cls.slug == chart_slug,
            )
            .one_or_none()
        )

    @classmethod
    def get(cls, id=None, mix_slug=None, song_slug=None, chart_slug=None):
        if mix_slug and song_slug and chart_slug:
            return cls.by_slug(mix_slug, song_slug, chart_slug)
        elif id:
            return cls.by_id(id)
        else:
            raise ValueError(
                "Either id or (mix_slug, song_slug, chart_slug) must be provided."
            )

    @classmethod
    def from_sim(cls, chart: BaseChart) -> "ChartRecord":
        return cls(
            stepstype=chart.stepstype,
            description=chart.description,
            difficulty=chart.difficulty,
            rating=0,
        )


@event.listens_for(ChartRecord, "before_insert")
def on_insert_chart(mapper, conn, target):
    target.slug = slugify(_generate_chart_slug(target.stepstype, target.difficulty))


@event.listens_for(ChartRecord, "before_update")
def on_update_chart(mapper, conn, target):
    if (
        inspect(target).attrs.stepstype.history.has_changes()
        or inspect(target).attrs.difficulty.history.has_changes()
    ):
        target.slug = slugify(_generate_chart_slug(target.stepstype, target.difficulty))


def _generate_chart_slug(stepstype: str, difficulty: str) -> str:
    if stepstype.startswith("dance-"):
        stepstype = stepstype[6:]
    return f"{stepstype}-{difficulty}".lower()
