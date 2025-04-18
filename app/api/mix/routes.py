from flask import Blueprint
from app.form.mix.create import MixCreateForm
from app.database import db

from app.utils.responses import json_error, json_success

mix_api_bp = Blueprint("mix_api", __name__)


@mix_api_bp.route("/create.json", methods=["POST"])
def create_mix():
    form = MixCreateForm()

    if form.validate_on_submit():
        mix = form.to_entity()

        with db.session.begin():
            if mix.banner:
                db.session.add(mix.banner)
                db.session.flush()
            db.session.add(mix)

        return json_success(
            "Mix created", {"id": str(mix.id), "slug": mix.slug}, status=201
        )

    return json_error("Validation failed", form.errors)
