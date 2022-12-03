import logging

import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

from app import create_app
from app.models import User
from config import Config

app = create_app()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(email=data['user_email']).first()
        except Exception as ex:
            logging.debug(ex)
            return jsonify({'message': 'Token is invalid !!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


def encode_access_token(user_id, email, plan):
    access_token = jwt.encode(
        {
            'user_id': user_id,
            'email': email,
            'plan': plan,
            'exp': datetime.utcnow() + timedelta(minutes=15),  # The token will expire in 15 minutes
        },
        app.config['SECRET_KEY'],
        algorithm='HS256',
    )

    return access_token


def encode_refresh_token(user_id, email, plan):
    refresh_token = jwt.encode(
        {
            'user_id': user_id,
            'email': email,
            'plan': plan,
            'exp': datetime.utcnow() + timedelta(weeks=4),  # The token will expire in 4 weeks
        },
        Config.SECRET_KEY,
        algorithm='HS256',
    )

    return refresh_token


def refresh_access_token(refresh_token):
    # If the refresh_token is still valid, create a new access_token and return it
    try:
        user = app.db.users.find_one(
            {'refresh_token': refresh_token}, {'_id': 0, 'id': 1, 'email': 1, 'plan': 1}
        )

        if user:
            decoded = jwt.decode(refresh_token, app.config['SECRET_KEY'])
            new_access_token = encode_access_token(
                decoded['user_id'], decoded['email'], decoded['plan']
            )
            result = jwt.decode(new_access_token, app.config['SECRET_KEY'])
            result['new_access_token'] = new_access_token
            resp = jsonify(result, 200)
        else:
            result = {'message': 'Auth refresh token has expired'}
            resp = jsonify(result, 403)

    except Exception as ex:
        logging.exception(ex)
        result = {'message': 'Auth refresh token has expired'}
        resp = jsonify(result, 403)

    return resp
