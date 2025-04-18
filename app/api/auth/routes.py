from flask import Blueprint, request, session, current_app
from app.utils.responses import json_success, json_error

auth_api_bp = Blueprint("auth_api", __name__)


@auth_api_bp.route("/login.json", methods=["POST"])
def login():
    key = request.json.get("api_key")
    expected = current_app.config["ADMIN_API_KEY"]

    if key == expected:
        session["is_admin"] = True
        return json_success("Logged in as admin")

    return json_error("Invalid API key", 401)


@auth_api_bp.route("/logout.json", methods=["POST"])
def logout():
    session.clear()
    return json_success("Logged out")
