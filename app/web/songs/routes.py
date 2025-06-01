from typing import Any, cast
from flask import Blueprint, redirect, render_template, request, url_for
from app.models.mix_record import MixRecord
from app.models.song_record import SongRecord
from app.parser.load import load_simfile
from app.utils.content_route import content_route, request_is_json
from app.utils.query_arguments import get_single_query_arg
from app.utils.request_format import get_request_data
from app.utils.response_format import respond
from app.utils.responses import json_data, json_error
from app.web.auth.guard import require_admin
from app.database import db

song_bp = Blueprint("songs", __name__)


@content_route(song_bp, "/songs")
def index():
    mix_id = get_single_query_arg("mix_id")
    mix_title = get_single_query_arg("mix_title")

    if mix_id or mix_title:
        mix = None
        if mix_id:
            mix = MixRecord.get(mix_id)
        elif mix_title:
            matches = MixRecord.query.filter(MixRecord.title == mix_title).all()
            if len(matches) == 1:
                mix = matches[0]

        if mix:
            query_params = dict(request.args)
            for key in ["mix_id", "mix_title"]:
                query_params.pop(key, None)
            return redirect(
                url_for("mixes.show", id=mix.slug, **cast(dict[str, Any], query_params))
            )

    extra_fields = {
        "mix_title": ("text", MixRecord.title),
        "mix_id": ("id", [MixRecord.id, MixRecord.slug]),
        "release": ("date", MixRecord.release),
    }

    query = SongRecord.query_with_filters(request.args, extra_fields=extra_fields)
    songs = query.order_by(SongRecord.title).all()

    if request_is_json():
        return json_data(songs)

    title_terms = request.args.getlist("title")
    if len(title_terms) == 1:
        term = title_terms[0].lower()
        matches = [song for song in songs if song.title.lower() == term]
        if len(matches) == 1:
            return redirect(url_for("songs.show", id=matches[0].slug))

    return render_template("songs/index.html", songs=songs)


@song_bp.route("/songs/create")
def create():
    mixes = MixRecord.query.order_by(MixRecord.release.desc()).all()
    return render_template("songs/create.html", mixes=mixes)


@content_route(song_bp, "/songs/create", methods=["POST"])
@require_admin
def create_song():
    data = get_request_data()
    simfile_text = data.get("simfile_text")
    mix_id = data.get("mix_id")

    if not simfile_text or not mix_id:
        return respond(
            {"error": "Simfile and mix required", "form_data": request.form},
            template="songs/create.html",
            status=400,
        )

    try:
        record = load_simfile(simfile_text)
        record.song.mix_id = mix_id  # type: ignore
        db.session.add(record)
        db.session.commit()
        return respond(
            {"id": str(record.id), "slug": record.song.slug},
            template="songs/show.html",
            status=201,
        )
    except Exception as e:
        db.session.rollback()
        return respond(
            {"error": "Failed to create song", "form_data": request.form},
            template="songs/create.html",
            status=400,
        )


@content_route(song_bp, "/songs/<id>")
def show(id):
    song = SongRecord.get(id)

    if not song:
        return respond(
            {"error": "Song not found"},
            template="error/404.html",
            status=404,
        )

    if request_is_json():
        return json_data(song)

    return render_template("songs/show.html", song=song)


@song_bp.route("/songs/autocomplete.json")
def song_autocomplete():
    field = request.args.get("field")
    query = request.args.get("query", "").strip()
    limit = int(request.args.get("limit", 10))

    if field not in {"title", "artist"}:
        return json_error("Invalid field for autocomplete", status=400)

    suggestions = SongRecord.get_autocomplete(field, query=query, limit=limit)
    return json_data(suggestions)
