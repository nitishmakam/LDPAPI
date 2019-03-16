from functools import wraps

from flask import request, jsonify

import jwt

from app import app


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("token")
        if not token:
            return jsonify({"message": "Token is missing!"}), 403  # 403 error
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except Exception as e:
            return jsonify({"message": "Token is invalid!"}), 403  # 403 error

        return f(*args, **kwargs)

    return decorated
