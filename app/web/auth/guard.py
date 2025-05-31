from functools import wraps
from flask import request, session, current_app, jsonify, redirect, url_for, flash
from flask_wtf.csrf import validate_csrf, CSRFError

from app.utils.shape import wants_json


def is_authorized_request() -> bool:
    if session.get("is_admin"):
        if request.method in {"POST", "PUT", "PATCH", "DELETE"} and wants_json():
            try:
                validate_csrf(request.headers.get("X-CSRF-Token"))
            except CSRFError:
                return False
        return True

    api_key = request.headers.get("X-API-Key") or request.args.get("api_key")
    expected = current_app.config.get("ADMIN_KEY")
    return api_key == expected


def require_admin(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if is_authorized_request():
            return f(*args, **kwargs)

        wants_json = (
            request.path.endswith(".json")
            or request.accept_mimetypes["application/json"]
            > request.accept_mimetypes["text/html"]
        )

        if wants_json:
            return jsonify({"status": "error", "message": "Unauthorized"}), 401
        else:
            flash("You must be logged in as admin.", "error")
            return redirect(url_for("auth.login_page", next=request.path))

    return wrapper
