from flask import jsonify
from flask_restx import Resource, Namespace
from flask_sqlalchemy_session import current_session
from app.models import User

api = Namespace('users', description='People who use the app')


@api.route('/')
class Users(Resource):
    @api.response(200, 'Success')
    def get(self):
        users = current_session.session.query(User).all()
        response_list = []
        for row in users:
            response_list.append(row.to_dict())
        return jsonify(response_list)
