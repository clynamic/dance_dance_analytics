import uuid
from flask import Blueprint, abort, jsonify, redirect, render_template, request, url_for
from app.models.mix_record import MixRecord
from app.models.song_record import SongRecord
from app.parser.load import load_simfile
from app.utils.content_route import content_route, get_request_format
from app.utils.query_builder import build_dynamic_query
from app.utils.request_format import get_request_data
from app.utils.response_format import respond
from app.utils.responses import json_data
from app.web.auth.guard import require_admin
from app.database import db

song_bp = Blueprint("song", __name__)


@content_route(song_bp, "/song")
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

    if get_request_format() == "json":
        return json_data(songs)

    title_terms = request.args.getlist("title")
    if title_terms:
        for song in songs:
            if any(song.title.lower() == term.lower() for term in title_terms):
                return redirect(url_for("song.show", id=song.slug))

    return render_template(
        "song/index.html",
        songs=songs,
        title_suggestions=SongRecord.get_autocomplete("title"),
        artist_suggestions=SongRecord.get_autocomplete("artist"),
        mix_title_suggestions=MixRecord.get_autocomplete("title"),
    )


@song_bp.route("/song/create")
def create():
    mixes = MixRecord.query.order_by(MixRecord.release.desc()).all()
    return render_template("song/create.html", mixes=mixes)


@content_route(song_bp, "/song/create", methods=["POST"])
@require_admin
def create_song():
    data = get_request_data()
    simfile_text = data.get("simfile_text")
    mix_id = data.get("mix_id")

    if not simfile_text or not mix_id:
        return respond(
            {"error": "Simfile and mix required", "form_data": request.form},
            template="song/create.html",
            status=400,
        )

    try:
        record = load_simfile(simfile_text)
        record.song.mix_id = mix_id  # type: ignore
        db.session.add(record)
        db.session.commit()
        return respond(
            {"id": str(record.id), "slug": record.song.slug},
            template="song/show.html",
            status=201,
        )
    except Exception as e:
        db.session.rollback()
        return respond(
            {"error": "Failed to create song", "form_data": request.form},
            template="song/create.html",
            status=400,
        )


@content_route(song_bp, "/song/<id>")
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
        return respond(
            {"error": "Song not found"},
            template="error/404.html",
            status=404,
        )

    if get_request_format() == "json":
        return json_data(song)

    return render_template("song/show.html", song=song)
