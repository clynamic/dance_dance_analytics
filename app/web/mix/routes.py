from flask import Blueprint, redirect, render_template, request, url_for
from flask import Blueprint, render_template, abort
from app.form.mix.create import MixCreateForm
from app.form.mix.edit import MixEditForm
from app.utils.content_route import content_route, get_request_format
from app.utils.response_format import respond
from app.utils.responses import json_data, json_error, json_success
from app.web.auth.guard import require_admin
from app.models.mix_record import MixRecord
from app.database import db
import uuid

from app.utils.query_builder import build_dynamic_query

mix_bp = Blueprint("mix", __name__)


@content_route(mix_bp, "/mix")
def index():
    query = MixRecord.query

    QUERY_FIELDS = {
        "title": ("text", MixRecord.title),
        "system": ("text", MixRecord.system),
        "region": ("text", MixRecord.region),
        "id": ("id", [MixRecord.id, MixRecord.slug]),
        "release": ("date", MixRecord.release),
    }

    query = build_dynamic_query(query, request.args, QUERY_FIELDS)

    mixes = query.order_by(MixRecord.release.desc()).all()

    if get_request_format() == "json":
        return json_data(mixes)

    title_terms = request.args.getlist("title")
    if title_terms:
        for mix in mixes:
            if any(mix.title.lower() == term.lower() for term in title_terms):
                return redirect(url_for("mix.show", id=mix.slug))

    return render_template("mix/index.html", mixes=mixes)


@mix_bp.route("/mix/create")
@require_admin
def create():
    return render_template("mix/create.html")


@mix_bp.route("/mix/create.json", methods=["POST"])
@require_admin
def create_mix():
    form = MixCreateForm()

    if form.validate_on_submit():
        mix = form.to_entity()

        if mix.banner:
            db.session.add(mix.banner)
            db.session.flush()
        db.session.add(mix)
        db.session.commit()

        return json_success(
            "Mix created", {"id": str(mix.id), "slug": mix.slug}, status=201
        )

    return json_error("Validation failed", form.errors)


@content_route(mix_bp, "/mix/<id>")
def show(id):
    mix = None

    try:
        mix_id = uuid.UUID(id)
        mix = MixRecord.get(mix_id)
    except (ValueError, IndexError):
        pass

    if mix is None:
        mix = MixRecord.query.filter_by(slug=id).first()

    if not mix:
        return respond(
            {"error": "Mix not found"},
            template="error/404.html",
            status=404,
        )

    if get_request_format() == "json":
        return json_data(mix)

    return render_template("mix/show.html", mix=mix)


@mix_bp.route("/mix/<id>/edit")
@require_admin
def edit(id):
    mix = MixRecord.get(id)

    if not mix:
        abort(404)

    return render_template("mix/edit.html", mix=mix)


@mix_bp.route("/mix/<id>.json", methods=["PATCH"])
@require_admin
def edit_mix(id):
    mix = MixRecord.get(id)
    if not mix:
        return json_error("Mix not found", status=404)

    form = MixEditForm()

    if form.validate_on_submit():
        form.update_entity(mix)

        if mix.banner:
            db.session.add(mix.banner)
            db.session.flush()
        db.session.add(mix)
        db.session.commit()

        return json_success(
            "Mix updated", {"id": str(mix.id), "slug": mix.slug}, status=200
        )

    return json_error("Validation failed", form.errors)


@mix_bp.route("/mix/autocomplete.json")
def mix_autocomplete():
    field = request.args.get("field")
    query = request.args.get("query", "").strip()
    limit = int(request.args.get("limit", 10))

    if field not in {"system", "region", "title"}:
        return json_error("Invalid field for autocomplete", status=400)

    suggestions = MixRecord.get_autocomplete(field, query=query, limit=limit)
    return json_data(suggestions)
