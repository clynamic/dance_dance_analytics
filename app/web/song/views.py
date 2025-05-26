import uuid
from flask import Blueprint, abort, render_template
from app.models.mix_record import MixRecord
from app.models.song_record import SongRecord

song_web_bp = Blueprint("song_web", __name__)


@song_web_bp.route("/")
def index():
    songs = SongRecord.query.order_by(SongRecord.title.desc()).all()
    return render_template("song/index.html", songs=songs)


@song_web_bp.route("/create")
def upload_page():
    mixes = MixRecord.query.order_by(MixRecord.release.desc()).all()
    return render_template("song/create.html", mixes=mixes)


@song_web_bp.route("/<id>")
def show(id):
    song = None

    try:
        song_id = uuid.UUID(id)
        song = SongRecord.query.get(song_id)
    except (ValueError, IndexError):
        pass

    if song is None:
        song = SongRecord.query.filter_by(slug=id).first()

    if not song:
        abort(404)

    return render_template("song/show.html", song=song)
