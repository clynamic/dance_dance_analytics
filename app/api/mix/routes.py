from flask import Blueprint, request, jsonify
from app.models.mix_record import MixRecord
from app.models.banner_record import BannerRecord
from app.database import db
import uuid
from datetime import datetime

mix_api_bp = Blueprint("mix_api", __name__)


@mix_api_bp.route("/create.json", methods=["POST"])
def create_mix():
    try:
        title = request.form["title"]
        system = request.form["system"]
        region = request.form["region"]
        release_str = request.form["release"]
        banner_file = request.files.get("banner")

        release_date = datetime.strptime(release_str, "%Y-%m-%d").date()

        with db.session.begin():
            banner = None
            if banner_file:
                banner = BannerRecord(blob=banner_file.read())
                db.session.add(banner)
                db.session.flush()

            mix = MixRecord(
                id=uuid.uuid4(),
                title=title,
                system=system,
                region=region,
                release=release_date,
                banner=banner,
            )

            db.session.add(mix)

        return jsonify({"status": "ok", "mix_id": str(mix.id)}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
