from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask import Blueprint, render_template, abort
from app.form.mixes.create import MixCreateForm
from app.form.mixes.edit import MixEditForm
from app.models.song_record import SongRecord
from app.utils.responses import model_route, request_is_json, respond
from app.utils.responses import json_data, json_error, json_success
from app.web.auth.guard import require_admin
from app.models.mix_record import MixRecord
from app.database import db


mix_bp = Blueprint("mixes", __name__)


@mix_bp.route("/mixes/create")
@require_admin
def create():
    form = MixCreateForm()

    return render_template("mixes/create.html", form=form)


@model_route(mix_bp, "/mixes/create", methods=["POST"])
@require_admin
def create_cmd():
    form = MixCreateForm()

    if not form.validate_on_submit():
        errors = form.errors
        if request.is_json:
            return json_error("Validation failed", errors)

        return render_template("mixes/create.html", form=form, errors=errors)

    mix = form.to_entity()
    db.session.add(mix)
    db.session.commit()

    if request.is_json:
        return json_success(
            "Mix created", {"id": str(mix.id), "slug": mix.slug}, status=201
        )
    flash("Mix created successfully", "success")
    return redirect(url_for("mixes.show", slug=mix.slug))


@model_route(mix_bp, "/mixes", endpoint="index")
def index():
    query = MixRecord.query_with_filters(request.args)

    mixes = query.order_by(MixRecord.release.desc()).all()

    if request_is_json():
        return json_data(mixes)

    title_terms = request.args.getlist("title")
    if title_terms:
        for mix in mixes:
            if any(mix.title.lower() == term.lower() for term in title_terms):
                return redirect(url_for("mixes.show", slug=mix.slug))

    return render_template("mixes/index.html", mixes=mixes)


@model_route(mix_bp, "/mixes/<id>", endpoint="show_by_id")
@model_route(mix_bp, "/<slug>", endpoint="show")
def show(id=None, slug=None):
    mix = MixRecord.get(slug=slug, id=id)

    if not mix:
        return respond(
            {"error": "Mix not found"},
            template="error/404.html",
            status=404,
        )

    if request_is_json():
        return json_data(mix)

    query = SongRecord.query_with_filters(request.args)
    query = query.filter(SongRecord.mix_id == mix.id)

    songs = query.order_by(SongRecord.title).all()

    return render_template("songs/index.html", songs=songs, mix=mix)


@mix_bp.route("/mixes/<id>/edit", endpoint="edit_by_id")
@mix_bp.route("/<slug>/edit", endpoint="edit")
@require_admin
def edit(id=None, slug=None):
    mix = MixRecord.get(slug=slug, id=id)

    if not mix:
        abort(404)

    form = MixEditForm()

    return render_template("mixes/edit.html", mix=mix, form=form)


@model_route(mix_bp, "/mixes/<id>/edit", methods=["PATCH"], endpoint="edit_cmd_by_id")
@model_route(mix_bp, "/<slug>/edit", methods=["PATCH"], endpoint="edit_cmd")
@require_admin
def edit_cmd(id=None, slug=None):
    mix = MixRecord.get(slug=slug, id=id)

    if not mix:
        return respond(
            {"error": "Mix not found"},
            template="error/404.html",
            status=404,
        )

    form = MixEditForm()

    if not form.validate_on_submit():
        errors = form.errors
        if request.is_json:
            return json_error("Validation failed", errors)

        return render_template("mixes/edit.html", form=form, mix=mix, errors=errors)

    update = form.update_entity(mix)
    db.session.add(update)

    if request.is_json:
        return json_success(
            "Mix updated", {"id": str(mix.id), "slug": mix.slug}, status=200
        )

    flash("Mix updated successfully", "success")
    return redirect(url_for("mixes.show", slug=mix.slug))


@model_route(
    mix_bp, "/mixes/<id>/delete", methods=["DELETE"], endpoint="delete_cmd_by_id"
)
@model_route(mix_bp, "/<slug>/delete", methods=["DELETE"], endpoint="delete_cmd")
@require_admin
def delete_cmd(id=None, slug=None):
    mix = MixRecord.get(slug=slug, id=id)

    if not mix:
        return respond(
            {"error": "Mix not found"},
            template="error/404.html",
            status=404,
        )

    db.session.delete(mix)
    db.session.commit()

    if request.is_json:
        return json_success("Mix deleted successfully", status=204)

    flash("Mix deleted successfully", "success")
    return redirect(url_for("mixes.index"))


@mix_bp.route("/mixes/autocomplete.json")
def autocomplete():
    field = request.args.get("field")
    query = request.args.get("query", "").strip()
    limit = int(request.args.get("limit", 10))

    if field not in {"system", "region", "title"}:
        return json_error("Invalid field for autocomplete", status=400)

    suggestions = MixRecord.get_autocomplete(field, query=query, limit=limit)
    return json_data(suggestions)
