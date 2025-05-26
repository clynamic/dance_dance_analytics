from flask import Flask

from app.utils.csrf import init_csrf_cookie
from app.utils.empty_query import strip_empty_query_params
from app.utils.partials import inject_partials
from .database import db
from .api.routes import api_bp
from .web.views import web_bp
from .web.mix.views import mix_web_bp
from .api.mix.routes import mix_api_bp
from .api.assets.routes import assets_bp
from .api.auth.routes import auth_api_bp
from .web.auth.views import auth_web_bp
from .web.song.views import song_web_bp
from .api.song.routes import song_api_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    init_csrf_cookie(app)

    @app.before_request
    def _():
        return strip_empty_query_params()

    @app.after_request
    def _(response):
        return inject_partials(response)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    api_bp.register_blueprint(mix_api_bp, url_prefix="/mix")
    web_bp.register_blueprint(mix_web_bp, url_prefix="/mix")

    api_bp.register_blueprint(song_api_bp, url_prefix="/song")
    web_bp.register_blueprint(song_web_bp, url_prefix="/song")

    app.register_blueprint(assets_bp, url_prefix="/cdn")

    api_bp.register_blueprint(auth_api_bp, url_prefix="/auth")
    web_bp.register_blueprint(auth_web_bp)

    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
