from typing import Any
from flask.typing import ResponseReturnValue
from werkzeug.exceptions import HTTPException
import traceback
from flask import Blueprint, jsonify, render_template, request, current_app
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


@web_bp.errorhandler(Exception)
def handle_api_exception(e) -> ResponseReturnValue:
    is_dev = current_app.config.get("ENV") == "development"

    if isinstance(e, HTTPException):
        return json_error(e.description or "An error occurred", e.code)

    message = "Unexpected server error"
    debug = None

    if is_dev:
        debug = {
            "type": type(e).__name__,
            "message": str(e),
            "traceback": traceback.format_exc().splitlines(),
        }

    return json_error(
        message,
        errors=debug,
        status=500,
    )


@web_bp.route("/")
def index():
    return redirect(url_for("mixes.index"))
