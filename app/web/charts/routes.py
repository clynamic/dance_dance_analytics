from typing import Any, cast
from flask import Blueprint, render_template, request, redirect, url_for
from app.models.mix_record import MixRecord
from app.models.song_record import SongRecord
from app.models.chart_record import ChartRecord
from app.utils.responses import model_route, request_is_json
from app.utils.responses import json_data, respond

chart_bp = Blueprint("charts", __name__)


@chart_bp.route("/charts")
def index():
    song_id = request.args.get("song_id")
    song_title = request.args.get("song_title")

    song = None
    if song_id:
        song = SongRecord.get(id=song_id)
    elif song_title:
        matches = SongRecord.query.filter(SongRecord.title == song_title).all()
        if len(matches) == 1:
            song = matches[0]

    if song:
        query_params = dict(request.args)
        query_params.pop("song_id", None)
        query_params.pop("song_title", None)
        return redirect(
            url_for(
                "songs.show",
                mix_slug=song.mix.slug,
                song_slug=song.slug,
                **cast(dict[str, Any], query_params)
            )
        )

    extra_fields = {
        "song_title": ("text", SongRecord.title),
        "song_id": ("id", [SongRecord.id, SongRecord.slug]),
    }

    query = ChartRecord.query_with_filters(request.args, extra_fields=extra_fields)
    charts = query.order_by(ChartRecord.difficulty).all()

    if request_is_json():
        return json_data(charts)

    return render_template("charts/index.html", charts=charts)


@model_route(chart_bp, "/charts/<id>", endpoint="show_by_id")
@model_route(chart_bp, "/<mix_slug>/<song_slug>/<chart_slug>", endpoint="show")
def show(id=None, mix_slug=None, song_slug=None, chart_slug=None):
    chart = ChartRecord.get(
        id=id, mix_slug=mix_slug, song_slug=song_slug, chart_slug=chart_slug
    )

    if not chart:
        return respond(
            {"error": "Chart not found"}, template="error/404.html", status=404
        )

    if request_is_json():
        return json_data(chart)

    return render_template(
        "charts/show.html", chart=chart, song=chart.song, mix=chart.song.mix
    )
