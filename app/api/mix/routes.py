from flask import Blueprint
from app.api.auth.guard import require_admin
from app.form.mix.create import MixCreateForm
from app.database import db

from app.form.mix.edit import MixEditForm
from app.models.mix_record import MixRecord
from app.utils.responses import json_error, json_success

mix_api_bp = Blueprint("mix_api", __name__)


@mix_api_bp.route("/create.json", methods=["POST"])
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


@mix_api_bp.route("/<id>.json", methods=["PATCH"])
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
