from flask import Blueprint, render_template, request
from flask import render_template, redirect, url_for
from app.utils.responses import json_error

web_bp = Blueprint("web", __name__)


@web_bp.app_errorhandler(404)
def not_found(_):
    if (
        request.path.endswith(".json")
        or request.accept_mimetypes["application/json"]
        > request.accept_mimetypes["text/html"]
    ):
        return json_error("Not found", 404)

    return render_template("error/404.html"), 404


@web_bp.route("/")
def index():
    return redirect(url_for("web.mix_web.index"))
