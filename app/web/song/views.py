from flask import Blueprint, render_template
from app.models.mix_record import MixRecord

song_web_bp = Blueprint("song_web", __name__)


@song_web_bp.route("/create")
def upload_page():
    mixes = MixRecord.query.order_by(MixRecord.release.desc()).all()
    return render_template("song/create.html", mixes=mixes)
