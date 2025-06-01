from flask_migrate import Migrate
from flask import Flask

from app.utils.csrf import init_csrf_cookie
from app.utils.empty_query import strip_empty_query_params
from app.utils.partials import inject_partials
from .database import db
from app.web.routes import web_bp
from app.web.mixes.routes import mix_bp
from app.web.songs.routes import song_bp
from app.web.charts.routes import chart_bp
from app.web.assets.routes import assets_bp
from app.web.auth.routes import auth_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    init_csrf_cookie(app)

    app.before_request(strip_empty_query_params)
    app.after_request(inject_partials)

    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(web_bp)
    app.register_blueprint(mix_bp)
    app.register_blueprint(song_bp)
    app.register_blueprint(chart_bp)
    app.register_blueprint(assets_bp)
    app.register_blueprint(auth_bp)

    return app
