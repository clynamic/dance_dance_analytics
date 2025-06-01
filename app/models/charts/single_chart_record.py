from app.database import db


class SingleChartRecord(db.Model):
    __tablename__ = "single_chart_records"

    id = db.Column(db.Uuid, db.ForeignKey("chart_records.id"), primary_key=True)
    chart = db.relationship("ChartRecord", back_populates="single_chart", uselist=False)

    length_seconds = db.Column(db.Float)
    display_bpm_min = db.Column(db.Float)
    display_bpm_max = db.Column(db.Float)
    true_bpm_min = db.Column(db.Float)
    true_bpm_max = db.Column(db.Float)
    bpm_changes = db.Column(db.Integer)

    steps = db.Column(db.Integer)
    jumps = db.Column(db.Integer)
    holds = db.Column(db.Integer)
    shock_arrows = db.Column(db.Integer)
    hands = db.Column(db.Integer)
    crossovers = db.Column(db.Integer)
    footswitches = db.Column(db.Integer)
    sideswitches = db.Column(db.Integer)
    jacks = db.Column(db.Integer)
    brackets = db.Column(db.Integer)
    total_stream = db.Column(db.Integer)
    max_nps = db.Column(db.Float)
