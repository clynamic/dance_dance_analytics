from flask import Blueprint, render_template
from flask import Blueprint, render_template, abort
from app.api.auth.guard import require_admin
from app.database import db
from app.models.mix_record import MixRecord
import uuid

mix_web_bp = Blueprint("mix_web", __name__)


@mix_web_bp.route("/")
def index():
    mixes = db.session.query(MixRecord).order_by(MixRecord.release.desc()).all()
    return render_template("mix/index.html", mixes=mixes)


@mix_web_bp.route("/create")
@require_admin
def create():
    return render_template(
        "mix/create.html",
        region_suggestions=MixRecord.get_region_autocomplete(),
        system_suggestions=MixRecord.get_system_autocomplete(),
    )


@mix_web_bp.route("/<id>")
def show(id):
    mix = None

    try:
        mix_id = uuid.UUID(id)
        mix = MixRecord.query.get(mix_id)
    except (ValueError, IndexError):
        pass

    if mix is None:
        mix = MixRecord.query.filter_by(slug=id).first()

    if not mix:
        abort(404)

    return render_template("mix/show.html", mix=mix)
