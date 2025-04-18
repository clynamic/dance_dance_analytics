from flask import Blueprint, abort, jsonify, request

from app.api.auth import check_auth
from app.parser.load import load_simfile

from flask import jsonify, current_app
from werkzeug.exceptions import HTTPException
import traceback


api_bp = Blueprint("api", __name__)


@api_bp.errorhandler(Exception)
def handle_api_exception(e):
    is_dev = current_app.config.get("ENV") == "development"

    if isinstance(e, HTTPException):
        return jsonify({"status": "error", "message": e.description}), e.code

    response = {
        "status": "error",
        "message": "Unexpected server error",
    }

    if is_dev:
        response["debug"] = {
            "type": type(e).__name__,
            "message": str(e),
            "traceback": traceback.format_exc().splitlines(),
        }

    return jsonify(response), 500


@api_bp.route("/upload.json", methods=["POST"])
def upload_simfile():
    check_auth()

    simfile_text = request.data.decode("utf-8").strip()
    if not simfile_text:
        abort(400, description="Empty simfile")

    try:
        record = load_simfile(simfile_text)
        return (
            jsonify(
                {
                    "status": "ok",
                    "hash": record.hash,
                    "id": str(record.id),
                }
            ),
            201,
        )
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
