from flask import Blueprint, render_template

auth_web_bp = Blueprint("auth_web", __name__)


@auth_web_bp.route("/login")
def login_page():
    return render_template("auth/login.html")


@auth_web_bp.route("/logout")
def logout_page():
    return render_template("auth/logout.html")
