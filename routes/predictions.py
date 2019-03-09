from flask import Blueprint
import jwt
from app import app
prediction = Blueprint("prediction", __name__, url_prefix="/prediction")


@prediction.route("/", methods=['GET'])
def index():
    if (not request.json['token']):
        try:
            jwt.decode(request.json['token'], app.config.get('SECRET_KEY'))
        except jwt.ExpiredSignatureError:
            return "", 403
        except jwt.InvalidTokenError:
            return "", 403
    return "Hello,Prediction!"