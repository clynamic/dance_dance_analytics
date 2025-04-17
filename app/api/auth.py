from flask import request, abort
import os

API_KEY = os.getenv("API_KEY")


def check_auth():
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer ") and auth_header[7:] == API_KEY:
        return

    cookie_key = request.cookies.get("api_key")
    if cookie_key == API_KEY:
        return

    abort(401, description="Unauthorized")
