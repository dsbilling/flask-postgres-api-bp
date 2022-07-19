from flask import Blueprint

stocks_blueprint = Blueprint('stocks', __name__)

from . import routes