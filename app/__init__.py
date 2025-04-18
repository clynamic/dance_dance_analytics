from flask import Flask
from .database import db
from .api.routes import api_bp
from .web.views import web_bp
from .web.mix.views import mix_web_bp
from .api.mix.routes import mix_api_bp
from .api.assets.routes import assets_bp
from .api.auth.routes import auth_api_bp
from .web.auth.views import auth_web_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    with app.app_context():
        db.create_all()

    api_bp.register_blueprint(mix_api_bp, url_prefix="/mix")
    web_bp.register_blueprint(mix_web_bp, url_prefix="/mix")

    app.register_blueprint(assets_bp, url_prefix="/cdn")

    api_bp.register_blueprint(auth_api_bp, url_prefix="/auth")
    web_bp.register_blueprint(auth_web_bp)

    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
