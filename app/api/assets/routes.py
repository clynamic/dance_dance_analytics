from flask import Blueprint, abort, send_file
from io import BytesIO
from app.models.banner_record import BannerRecord

assets_bp = Blueprint("assets_api", __name__)


@assets_bp.route("/banner/<uuid:id>")
def get_banner(id):
    banner = BannerRecord.query.get(id)
    if not banner or not banner.blob:
        abort(404)

    return send_file(
        BytesIO(banner.blob),
        mimetype="image/png",
        as_attachment=False,
    )
