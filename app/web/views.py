from flask import Blueprint, render_template
from flask import render_template
from app.models.mix_record import MixRecord
from app.database import db

web_bp = Blueprint("web", __name__)


@web_bp.app_errorhandler(404)
def not_found(_):
    return render_template("error/404.html"), 404


@web_bp.route("/")
def index():
    mixes = db.session.query(MixRecord).order_by(MixRecord.release.desc()).all()
    return render_template("index.html", mixes=mixes)


@web_bp.route("/upload")
def upload():
    return render_template("upload.html")
