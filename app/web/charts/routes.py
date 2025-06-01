from typing import Any, cast
from flask import Blueprint, redirect, render_template, request, url_for
from app.models.song_record import SongRecord
from app.models.chart_record import ChartRecord
from app.utils.content_route import content_route, request_is_json
from app.utils.query_arguments import get_single_query_arg
from app.utils.responses import json_data

from flask import Blueprint


chart_bp = Blueprint("charts", __name__)


@content_route(chart_bp, "/charts")
def index():
    song_id = get_single_query_arg("song_id")
    song_title = get_single_query_arg("song_title")

    if song_id or song_title:
        song = None
        if song_id:
            song = SongRecord.get(song_id)
        elif song_title:
            matches = SongRecord.query.filter(SongRecord.title == song_title).all()
            if len(matches) == 1:
                song = matches[0]

        if song:
            query_params = dict(request.args)
            for key in ["song_id", "song_title"]:
                query_params.pop(key, None)
            return redirect(
                url_for(
                    "songs.show", id=song.slug, **cast(dict[str, Any], query_params)
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

    title_terms = request.args.getlist("title")
    if len(title_terms) == 1:
        term = title_terms[0].lower()
        matches = [chart for chart in charts if chart.title.lower() == term]
        if len(matches) == 1:
            return redirect(url_for("charts.show", id=matches[0].slug))

    return render_template("charts/index.html", charts=charts)


@content_route(chart_bp, "/charts/<id>")
def show(id: str):
    chart = ChartRecord.get(id)
    if not chart:
        return redirect(url_for("charts.index"))

    if request_is_json():
        return json_data(chart)

    return render_template("charts/show.html", chart=chart)
