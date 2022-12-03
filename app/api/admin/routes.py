
from flask import current_app, abort, request
from . import admin_blueprint
from app.utils.apiutils import token_required


@admin_blueprint.before_request
@token_required
def admin_before_request(current_user):
    if current_user.user_type != 'Admin':
        current_app.logger.info(
            f'User {current_user.id} attempted to access an ADMIN page ({request.url}, {request.method})!')
        abort(403)


@admin_blueprint.route('/ping')
def test():
    return 'Pong'
