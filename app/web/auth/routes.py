from flask import Blueprint, render_template, request, session, current_app
from app.utils.responses import json_success, json_error

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/login")
def login_page():
    return render_template("auth/login.html")


@auth_bp.route("/auth/login.json", methods=["POST"])
def login():
    key = request.json.get("api_key")
    expected = current_app.config["ADMIN_KEY"]

    if key == expected:
        session["is_admin"] = True
        return json_success("Logged in as admin")

    return json_error("Invalid API key", 401)


@auth_bp.route("/auth/logout")
def logout_page():
    return render_template("auth/logout.html")


@auth_bp.route("/auth/logout.json", methods=["POST"])
def logout():
    session.clear()
    return json_success("Logged out")
