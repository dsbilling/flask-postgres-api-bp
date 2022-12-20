from config import Config
from flask import Flask
from .api import api_bp
from .ext import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(api_bp)
    return app
