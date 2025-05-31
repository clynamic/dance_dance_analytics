import uuid
from flask import Blueprint, abort, redirect, render_template, request, url_for
from app.models.mix_record import MixRecord
from app.models.song_record import SongRecord
from app.utils.query_builder import build_dynamic_query

song_web_bp = Blueprint("song_web", __name__)


@song_web_bp.route("/")
def index():
    query = SongRecord.query.join(MixRecord, SongRecord.mix_id == MixRecord.id)

    QUERY_FIELDS = {
        "title": ("text", SongRecord.title),
        "artist": ("text", SongRecord.artist),
        "mix_title": ("text", MixRecord.title),
        "mix": ("id", [MixRecord.id, MixRecord.slug]),
        "release": ("date", MixRecord.release),
    }

    query = build_dynamic_query(query, request.args, QUERY_FIELDS)

    songs = query.order_by(MixRecord.release.desc()).all()

    title_terms = request.args.getlist("title")
    if title_terms:
        for song in songs:
            if any(song.title.lower() == term.lower() for term in title_terms):
                return redirect(url_for("web.song_web.show", id=song.slug))

    return render_template(
        "song/index.html",
        songs=songs,
        title_suggestions=SongRecord.get_title_autocomplete(),
        artist_suggestions=SongRecord.get_artist_autocomplete(),
        mix_title_suggestions=MixRecord.get_title_autocomplete(),
    )


@song_web_bp.route("/create")
def create():
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
