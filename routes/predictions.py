from flask import Blueprint
import jwt
from app import app
from app.token_required import token_required
prediction = Blueprint("prediction", __name__, url_prefix="/prediction")


@prediction.route("/", methods=['GET'])
@token_required
def index():
    # if (not request.json['token']):
    #     try:
    #         jwt.decode(request.json['token'], app.config.get('SECRET_KEY'))
    #     except jwt.ExpiredSignatureError:
    #         return "", 403
    #     except jwt.InvalidTokenError:
    #         return "", 403
    return "Hello,Prediction!"