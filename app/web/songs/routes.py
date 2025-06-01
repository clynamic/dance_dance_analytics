from typing import Any, cast
from flask import Blueprint, flash, redirect, render_template, request, url_for
from app.form.songs.create import SongCreateForm
from app.models.chart_record import ChartRecord
from app.models.mix_record import MixRecord
from app.models.song_record import SongRecord
from app.utils.responses import model_route, request_is_json, respond
from app.utils.responses import json_data, json_error, json_success
from app.web.auth.guard import require_admin
from app.database import db

song_bp = Blueprint("songs", __name__)


@song_bp.route("/songs/create")
@require_admin
def create():
    form = SongCreateForm()
    mixes = MixRecord.query.order_by(MixRecord.release.desc()).all()
    return render_template("songs/create.html", mixes=mixes, form=form)


@model_route(song_bp, "/songs/create", methods=["POST"], endpoint="create_cmd")
@require_admin
def create_cmd():
    form = SongCreateForm()

    if not form.validate_on_submit():
        errors = form.errors
        if request_is_json():
            return json_error("Validation failed", errors)
        return render_template("songs/create.html", form=form, errors=errors)

    song = form.to_entity()
    db.session.add(song)
    db.session.commit()

    if request_is_json():
        return json_success(
            "Song created", {"id": str(song.id), "slug": song.slug}, status=201
        )

    flash("Song created successfully", "success")
    return redirect(url_for("songs.show", mix_slug=song.mix.slug, song_slug=song.slug))


@song_bp.route("/songs")
def index():
    mix_id = request.args.get("mix_id")
    mix_title = request.args.get("mix_title")

    mix = None
    if mix_id:
        mix = MixRecord.get(mix_id)
    elif mix_title:
        matches = MixRecord.query.filter(MixRecord.title == mix_title).all()
        if len(matches) == 1:
            mix = matches[0]

    if mix:
        query_params = dict(request.args)
        query_params.pop("mix_id", None)
        query_params.pop("mix_title", None)
        return redirect(
            url_for("mixes.show", slug=mix.slug, **cast(dict[str, Any], query_params))
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

    return render_template("songs/index.html", songs=songs)


@model_route(song_bp, "/songs/<id>", endpoint="show_by_id")
@model_route(song_bp, "/<mix_slug>/<song_slug>", endpoint="show")
def show(id=None, mix_slug=None, song_slug=None):
    song = SongRecord.get(id=id, mix_slug=mix_slug, song_slug=song_slug)

    if not song:
        return respond(
            {"error": "Song not found"}, template="error/404.html", status=404
        )

    if request_is_json():
        return json_data(song)

    charts = (
        ChartRecord.query.filter_by(song_id=song.id)
        .order_by(ChartRecord.difficulty)
        .all()
    )
    return render_template("charts/index.html", song=song, charts=charts)


@model_route(
    song_bp, "/songs/<id>/delete", methods=["DELETE"], endpoint="delete_cmd_by_id"
)
@model_route(
    song_bp, "/<mix_slug>/<song_slug>/delete", methods=["DELETE"], endpoint="delete_cmd"
)
@require_admin
def delete_cmd(id=None, mix_slug=None, song_slug=None):
    song = (
        SongRecord.get(id=id)
        if id
        else SongRecord.query.join(MixRecord)
        .filter(MixRecord.slug == mix_slug, SongRecord.slug == song_slug)
        .first()
    )

    if not song:
        return respond(
            {"error": "Song not found"}, template="error/404.html", status=404
        )

    db.session.delete(song)
    db.session.commit()

    if request_is_json():
        return json_success("Song deleted successfully", status=204)

    flash("Song deleted successfully", "success")
    return redirect(url_for("mixes.show", slug=song.mix.slug))


@song_bp.route("/songs/autocomplete.json")
def autocomplete():
    field = request.args.get("field")
    query = request.args.get("query", "").strip()
    limit = int(request.args.get("limit", 10))

    if field not in {"title", "artist"}:
        return json_error("Invalid field for autocomplete", status=400)

    suggestions = SongRecord.get_autocomplete(field, query=query, limit=limit)
    return json_data(suggestions)
