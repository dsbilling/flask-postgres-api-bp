import logging

from flask import Blueprint
from flask_restx import Api
from app.api.users.routes import api as users_ns

from config import Config

api_bp = Blueprint('api', __name__)
api = Api(api_bp, title=Config.SWAGGER_TITLE, description=Config.SWAGGER_DESCRIPTION, version=Config.SWAGGER_VERSION)
api.add_namespace(users_ns)


@api.errorhandler(Exception)
def default_error_handler(e):
    logging.exception(e)
    message = 'An unhandled exception occurred.'
    return {'message': message}, 500
