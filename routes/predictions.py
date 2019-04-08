from flask import Blueprint, request, make_response, jsonify
import jwt
from app import app
from app.token_required import token_required
prediction = Blueprint("prediction", __name__, url_prefix="/api/prediction")


@prediction.route("/generate", methods=['POST'])
# @token_required
def generate():
    # if (not request.json['token']):
    #     try:
    #         jwt.decode(request.json['token'], app.config.get('SECRET_KEY'))
    #     except jwt.ExpiredSignatureError:
    #         return "", 403
    #     except jwt.InvalidTokenError:
    #         return "", 403
    # return "Hello,Prediction!"
    print(request.json)
    return "", 200
