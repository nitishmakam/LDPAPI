from flask import Blueprint, request, make_response, jsonify
import jwt
import os
from app import app
from app.token_required import token_required
prediction = Blueprint("prediction", __name__, url_prefix="/prediction")
import pandas as pd
import lightgbm
import numpy


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


#
# Expects a comma separated string with 253 values
# Needs work
#
@token_required
@prediction.route("/generate", methods=['POST'])
def generate():
    row = request.json['row']
    df = pd.read_csv(pd.compat.StringIO(row), header=None)
    lgb_model = lightgbm.Booster(model_file=os.path.join(app.root_path,
        'files/lgb-model-1553308214.txt'))
    prediction = lgb_model.predict(df)
    return jsonify({"result": int(prediction.round().astype(numpy.int64)[0])})


#
# Returns an array of 20 comma separated strings
# Needs work
#
@prediction.route("/getrows", methods=['GET'])
def getrows():
    # need to change this to database access
    rows = pd.read_csv(os.path.join(app.root_path, 'files/sample.txt'),
            header=None)
    output = []
    for row in rows.values:
        output.append(str(",".join([str(e) for e in row])))
    return jsonify({"rows": output})

