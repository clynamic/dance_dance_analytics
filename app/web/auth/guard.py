from functools import wraps
from flask import request, session, current_app, redirect, url_for, flash

from app.utils.responses import request_is_json
from app.utils.responses import json_error


def is_authorized_request() -> bool:
    if session.get("is_admin"):
        return True

    auth_header = request.headers.get("Authorization")
    api_key = None
    if auth_header and auth_header.startswith("Bearer "):
        api_key = auth_header[len("Bearer ") :]
    else:
        api_key = request.headers.get("X-API-Key") or request.args.get("api_key")

    expected = current_app.config.get("ADMIN_KEY")
    return api_key == expected


def require_admin(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if is_authorized_request():
            return f(*args, **kwargs)

        if request_is_json():
            return json_error("Unauthorized", status=401)

        flash("You must be logged in as admin.", "error")
        return redirect(url_for("auth.login_page", next=request.path))

    return wrapper
