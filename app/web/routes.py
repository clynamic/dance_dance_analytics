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
def handle_api_exception(e):
    is_dev = current_app.config.get("ENV") == "development"

    if isinstance(e, HTTPException):
        return jsonify({"status": "error", "message": e.description}), e.code

    response = {
        "status": "error",
        "message": "Unexpected server error",
    }

    if is_dev:
        response["debug"] = {
            "type": type(e).__name__,
            "message": str(e),
            "traceback": traceback.format_exc().splitlines(),
        }

    return jsonify(response), 500


@web_bp.route("/")
def index():
    return redirect(url_for("mix.index"))
