from flask import Blueprint, request, make_response, jsonify
import jwt
import os
from app import app
from app.token_required import token_required
from app import mydb
from bson.objectid import ObjectId
predcoll = mydb["Prediction"]

import lightgbm as lgb
import numpy as np

prediction = Blueprint("prediction", __name__, url_prefix="/api/prediction")

#
# Assuming the attributes are all in the root of the json request
# Ignored the two drop down attributes for now
#
@prediction.route("/generate", methods=['POST'])
#@token_required
def generate():
    modelfiles = [
        "lgb-model-1555340227-0.txt",
        "lgb-model-1555340227-1.txt",
        "lgb-model-1555340227-2.txt",
        "lgb-model-1555340227-3.txt",
        "lgb-model-1555340227-4.txt",
    ]
    req = request.get_json()
    features = ["EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3", "DAYS_BIRTH", "DAYS_EMPLOYED", "AMT_ANNUITY", "AMT_CREDIT", "AMT_GOODS_PRICE", "DAYS_ID_PUBLISH", "DAYS_REGISTRATION", "DAYS_LAST_PHONE_CHANGE", "AMT_INCOME_TOTAL", "OWN_CAR_AGE", "REGION_POPULATION_RELATIVE", "HOUR_APPR_PROCESS_START", "AMT_REQ_CREDIT_BUREAU_YEAR", "AMT_REQ_CREDIT_BUREAU_QRT", "DEF_30_CNT_SOCIAL_CIRCLE", "YEARS_BEGINEXPLUATATION_MODE", "TOTALAREA_MODE", "OBS_60_CNT_SOCIAL_CIRCLE", "OBS_30_CNT_SOCIAL_CIRCLE", "BASEMENTAREA_MODE", "REGION_RATING_CLIENT_W_CITY", "APARTMENTS_MODE", "LANDAREA_AVG", "BASEMENTAREA_AVG", "DEF_60_CNT_SOCIAL_CIRCLE", "CODE_GENDER", "LANDAREA_MODE", "AMT_REQ_CREDIT_BUREAU_MON", "YEARS_BEGINEXPLUATATION_MEDI", "REG_CITY_NOT_LIVE_CITY", "NONLIVINGAREA_MEDI", "LANDAREA_MEDI", "BASEMENTAREA_MEDI", "COMMONAREA_MEDI", "YEARS_BEGINEXPLUATATION_AVG", "LIVINGAREA_MEDI", "CNT_FAM_MEMBERS"]
    row = []
    for feat in features:
        row.append(req[feat])
    row = np.asarray(row)
    row = row.reshape(1, row.shape[0])
    models = []
    for mf in modelfiles:
        models.append(
            lgb.Booster(model_file=os.path.join(app.root_path,
                'files/%s' % mf))
        )
    preds = []
    for model in models:
        preds.append(
            model.predict(row)[0]
        )
    result = {"p%d"%i:preds[i] for i in range(len(preds))}
    prediction = np.mean(preds)
    result["prediction"] = prediction
    return jsonify(result)

@prediction.route("/save", methods=['POST'])
#@token_required
def save():
    token = request.headers.get("token")
    decoded = jwt.decode(token, app.config["SECRET_KEY"])
    username = decoded.get("username")
    req = request.get_json()
    req["username"] = username
    predcoll.insert(req)
    return "", 200


@prediction.route("/", methods=['GET'])
#@token_required
def getPredictions():
    token = request.headers.get("token")
    decoded = jwt.decode(token, app.config["SECRET_KEY"])
    username = decoded.get("username")
    preds = predcoll.find({"username": username})
    results = [pred for pred in preds]
    for res in results:
        res["id"] = str(res["_id"])
        res.pop("_id")
    return jsonify(results)


@prediction.route("/<pid>", methods=['DELETE'])
#@token_required
def deletePrediction(pid=None):
    token = request.headers.get("token")
    decoded = jwt.decode(token, app.config["SECRET_KEY"])
    username = decoded.get("username")
    result = predcoll.delete_one({"_id": ObjectId(pid),
                                  "username": username})
    return "", 200 if result.deleted_count == 1 else 400
