from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    current_app,
    url_for,
)
from app.utils.content_route import content_route, request_is_json
from app.utils.responses import json_success, json_error

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/login")
def login_page():
    return render_template("auth/login.html")


@content_route(auth_bp, "/auth/login", methods=["POST"])
def login():
    key = (
        request.json.get("api_key") if request.is_json else request.form.get("api_key")
    )

    expected = current_app.config["ADMIN_KEY"]

    if not key:
        if request_is_json():
            return json_error("API key is required", 400)
        return render_template(
            "auth/login.html", errors={"api_key": "API key is required"}
        )

    if key != expected:
        if request_is_json():
            return json_error("Invalid API key", 403)
        return render_template("auth/login.html", errors={"api_key": "Invalid API key"})

    session["is_admin"] = True
    if request_is_json():
        return json_success("Logged in as admin")
    flash("You are now logged in as admin", "success")
    return redirect(url_for("web.index"))


@content_route(auth_bp, "/auth/logout", methods=["POST"])
def logout():
    session.clear()
    if request_is_json():
        return json_success("Logged out")
    flash("You have been logged out", "info")
    return redirect(url_for("web.index"))


@auth_bp.route("/admin")
def admin_page():
    if not session.get("is_admin"):
        flash("You must be logged in as admin to access this page", "warning")
        return redirect(url_for("auth.login_page"))
    return render_template("auth/admin.html")
