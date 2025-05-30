import uuid
from flask import Blueprint, abort, redirect, render_template, request, url_for
from app.form.song.index import SongIndexForm
from app.models.mix_record import MixRecord
from app.models.song_record import SongRecord

song_web_bp = Blueprint("song_web", __name__)


@song_web_bp.route("/")
def index():
    form = SongIndexForm(request.args)
    query = SongRecord.query.join(MixRecord, SongRecord.mix_id == MixRecord.id)

    if form.title.data:
        query = query.filter(SongRecord.title.ilike(f"%{form.title.data}%"))
    if form.artist.data:
        query = query.filter(SongRecord.artist.ilike(f"%{form.artist.data}%"))
    if form.mix_title.data:
        query = query.filter(MixRecord.title.ilike(f"%{form.mix_title.data}%"))

    songs = query.order_by(MixRecord.release.desc()).all()

    if form.title.data:
        for song in songs:
            if song.title.lower() == form.title.data.lower():
                return redirect(url_for("web.song_web.show", id=song.slug))

    return render_template(
        "song/index.html",
        songs=songs,
        form=form,
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
