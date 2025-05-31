from flask import Blueprint, abort, send_file
from io import BytesIO
from app.models.banner_record import BannerRecord

assets_bp = Blueprint("assets", __name__)


@assets_bp.route("/cdn/banner/<uuid:id>")
def get_banner(id):
    banner = BannerRecord.query.get(id)
    if not banner or not banner.blob:
        abort(404)

    return send_file(
        BytesIO(banner.blob),
        mimetype="image/png",
        as_attachment=False,
    )
