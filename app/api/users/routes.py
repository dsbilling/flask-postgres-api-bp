from flask_restx import Resource
from flask_restx import Namespace

api = Namespace('users', description='People who use the app')


@api.route('/')
class Users(Resource):
    @api.doc('list_users')
    def get(self):
        """Get all users"""
        return {'message': 'Hello World!'}
