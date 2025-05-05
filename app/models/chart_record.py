import uuid
from app.database import db


class ChartRecord(db.Model):
    __tablename__ = "chart_records"

    id = db.Column(db.Uuid, primary_key=True, default=uuid.uuid4)

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
