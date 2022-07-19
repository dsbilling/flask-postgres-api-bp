import jwt
from datetime import datetime
from functools import wraps
from flask import request, jsonify

from app import create_app
from app.models import User

app = create_app()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]

        if not token:
            return jsonify({"message": "Token is missing !!"}), 401

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = User.query.filter_by(email=data["user_email"]).first()
        except Exception as ex:
            print(ex)
            return jsonify({"message": "Token is invalid !!"}), 401

        return f(current_user, *args, **kwargs)

    return decorated


def encodeAccessToken(user_id, email, plan):

    accessToken = jwt.encode(
        {
            "user_id": user_id,
            "email": email,
            "plan": plan,
            "exp": datetime.datetime.utcnow()
            + datetime.timedelta(minutes=15),  # The token will expire in 15 minutes
        },
        app.config["SECRET_KEY"],
        algorithm="HS256",
    )

    return accessToken


def encodeRefreshToken(user_id, email, plan):

    refreshToken = jwt.encode(
        {
            "user_id": user_id,
            "email": email,
            "plan": plan,
            "exp": datetime.datetime.utcnow()
            + datetime.timedelta(weeks=4),  # The token will expire in 4 weeks
        },
        app.config["SECRET_KEY"],
        algorithm="HS256",
    )

    return refreshToken


def refreshAccessToken(refresh_token):

    # If the refresh_token is still valid, create a new access_token and return it
    try:
        user = app.db.users.find_one(
            {"refresh_token": refresh_token}, {"_id": 0, "id": 1, "email": 1, "plan": 1}
        )

        if user:
            decoded = jwt.decode(refresh_token, app.config["SECRET_KEY"])
            new_access_token = encodeAccessToken(
                decoded["user_id"], decoded["email"], decoded["plan"]
            )
            result = jwt.decode(new_access_token, app.config["SECRET_KEY"])
            result["new_access_token"] = new_access_token
            resp = JsonResp(result, 200)
        else:
            result = {"message": "Auth refresh token has expired"}
            resp = JsonResp(result, 403)

    except:
        result = {"message": "Auth refresh token has expired"}
        resp = JsonResp(result, 403)

    return resp
