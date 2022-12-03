from config import Config
from flask import Flask
from .api import api_bp
import logging
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()
db_migration = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)
    logging.basicConfig(level=logging.DEBUG)
    app.register_blueprint(api_bp, url_prefix='/')
    return app


def register_extensions(app):

    db = SQLAlchemy()
    migrate = Migrate()

    db.init_app(app)
    migrate.init_app(app, db)
