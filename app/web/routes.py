from flask.typing import ResponseReturnValue
from werkzeug.exceptions import HTTPException
import traceback
from flask import Blueprint, render_template, request, current_app
from flask import render_template
from app.utils.responses import json_error, request_is_json
from app.web.mixes import routes as mixes

web_bp = Blueprint("web", __name__)


@web_bp.app_errorhandler(Exception)
def handle_exception(e) -> ResponseReturnValue:
    is_dev = current_app.config.get("ENV") == "development"
    code = 500
    message = "Unexpected server error"
    debug = None

    if is_dev:
        traceback.print_exc()
    else:
        current_app.logger.error(f"Unhandled exception: {e}", exc_info=e)

    if isinstance(e, HTTPException):
        code = e.code if e.code else 500
        message = e.description or message

    if is_dev:
        debug = {
            "type": type(e).__name__,
            "message": str(e),
            "traceback": traceback.format_exc().splitlines(),
        }

    if request_is_json():
        return json_error(
            message,
            errors=debug,
            status=code,
        )

    template = (
        "error/404.html"
        if code == 404
        else "error/500.html" if code == 500 else "error/generic.html"
    )

    return render_template(template, message=message, debug=debug), code


@web_bp.route("/")
def index():
    return mixes.index()
