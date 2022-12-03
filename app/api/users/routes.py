import logging

from . import users_blueprint
from app.models import User
from app import database
from app import create_app

from datetime import datetime, timedelta

from flask import make_response, jsonify, request
import jwt

app = create_app()


@users_blueprint.route('/ping')
def test():
    return 'Users: Pong'


@users_blueprint.route('/signup', methods=['POST'])
def signup():
    data = request.form
    name, email = data.get('name'), data.get('email')
    password = data.get('password')

    # checking for existing user
    user = User.query.filter_by(email=email).first()

    if not user:
        user = User(name=name, email=email, password_plaintext=password)
        # insert user
        database.session.add(user)
        database.session.commit()

        return make_response('Successfully registered.', 201)
    else:
        return make_response('User already exists. Please Log in.', 202)


@users_blueprint.route('/login', methods=['POST'])
def login():
    auth = request.form

    if not auth or not auth.get('email') or not auth.get('password'):
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
        )

    user = User.query \
        .filter_by(email=auth.get('email')) \
        .first()

    if not user:
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
        )

    if user.is_password_correct(auth.get('password')):
        token = jwt.encode({
            'user_email': user.email,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, app.config['SECRET_KEY'])

        logging.debug(token)

        return make_response(jsonify({'token': token}), 201)

    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
    )


@users_blueprint.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()

    output = []
    for user in users:
        output.append({
            'name': user.name,
            'email': user.email,
            'password_plaintext': user.password_hashed,
            'user': user.user_type
        })

    return jsonify({'users': output})
