from flask import Blueprint, render_template
from flask import Blueprint, render_template, abort
from app.api.auth.guard import require_admin
from app.models.mix_record import MixRecord
import uuid

mix_web_bp = Blueprint("mix_web", __name__)


@mix_web_bp.route("/")
def index():
    mixes = MixRecord.query.order_by(MixRecord.release.desc()).all()
    return render_template("mix/index.html", mixes=mixes)


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
