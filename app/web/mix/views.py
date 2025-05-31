from flask import Blueprint, redirect, render_template, request, url_for
from flask import Blueprint, render_template, abort
from app.api.auth.guard import require_admin
from app.models.mix_record import MixRecord
import uuid

from app.utils.query_builder import build_dynamic_query

mix_web_bp = Blueprint("mix_web", __name__)


@mix_web_bp.route("/")
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

    title_terms = request.args.getlist("title")
    if title_terms:
        for mix in mixes:
            if any(mix.title.lower() == term.lower() for term in title_terms):
                return redirect(url_for("web.mix_web.show", id=mix.slug))

    return render_template(
        "mix/index.html",
        mixes=mixes,
        title_suggestions=[
            m.title for m in MixRecord.query.with_entities(MixRecord.title).all()
        ],
        system_suggestions=MixRecord.get_system_autocomplete(),
        region_suggestions=MixRecord.get_region_autocomplete(),
    )


@mix_web_bp.route("/create")
@require_admin
def create():
    return render_template(
        "mix/create.html",
        region_suggestions=MixRecord.get_region_autocomplete(),
        system_suggestions=MixRecord.get_system_autocomplete(),
    )


@mix_web_bp.route("/<id>/edit")
@require_admin
def edit(id):
    mix = MixRecord.get(id)

    if not mix:
        abort(404)

    return render_template(
        "mix/edit.html",
        mix=mix,
        region_suggestions=MixRecord.get_region_autocomplete(),
        system_suggestions=MixRecord.get_system_autocomplete(),
    )


@mix_web_bp.route("/<id>")
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
        abort(404)

    return render_template("mix/show.html", mix=mix)
