from config import DevelopmentConfig
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os


####################################
### Configuration           ########
####################################

database = SQLAlchemy()
db_migration = Migrate()


def create_app():

    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    initialize_extensions(app)
    register_blueprints(app)

    return app


def initialize_extensions(app):
    database.init_app(app)
    db_migration.init_app(app, database)


def register_blueprints(app):
    # Import the blueprints
    from app.api.stocks import stocks_blueprint
    from app.api.users import users_blueprint
    from app.api.admin import admin_blueprint

    app.register_blueprint(stocks_blueprint)
    app.register_blueprint(users_blueprint, url_prefix="/users")
    app.register_blueprint(admin_blueprint, url_prefix="/admin")
