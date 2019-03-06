from flask import Blueprint
from flask_jwt import jwt_required

prediction = Blueprint("prediction",__name__,url_prefix="/prediction")

@prediction.route("/")
def index():
    return "Hello,Prediction!"