from flask import Blueprint, request, jsonify, abort
from psycopg import IntegrityError
from app.api.auth.guard import require_admin
from app.database import db
from app.parser.load import load_simfile
from app.utils.responses import json_error, json_success

song_api_bp = Blueprint("song_api", __name__)


@song_api_bp.route("/create.json", methods=["POST"])
@require_admin
def create_song():
    simfile_text = request.data.decode("utf-8").strip()
    mix_id = request.args.get("mix_id")

    if not simfile_text:
        abort(400, description="Empty simfile")
    if not mix_id:
        abort(400, description="Missing mix_id")

    try:
        record = load_simfile(simfile_text)

        record.song.mix_id = mix_id

        db.session.add(record)
        db.session.commit()

        return json_success(
            "Song created",
            {"id": str(record.id), "slug": record.song.slug},
            status=201,
        )

    except IntegrityError as e:
        db.session.rollback()
        return json_error("Simfile import failed", {"error": str(e)}, status=400)

    except Exception as e:
        return json_error("Unexpected error", {"error": str(e)}, status=500)
