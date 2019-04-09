from flask import Blueprint, request, make_response, jsonify
import jwt
import os
from app import app
from app.token_required import token_required

import lightgbm as lgb
import numpy as np

prediction = Blueprint("prediction", __name__, url_prefix="/api/prediction")


# @prediction.route("/generate", methods=['POST'])
# # @token_required
# def generate():
#     # if (not request.json['token']):
#     #     try:
#     #         jwt.decode(request.json['token'], app.config.get('SECRET_KEY'))
#     #     except jwt.ExpiredSignatureError:
#     #         return "", 403
#     #     except jwt.InvalidTokenError:
#     #         return "", 403
#     # return "Hello,Prediction!"
#     print(request.json)
#     return "", 200



#
# Assuming the attributes are all in the root of the json request
# Ignored the two drop down attributes for now
#
@prediction.route("/generate", methods=['POST'])
#@token_required
def generate():
    req = request.get_json()
    features = ["EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3", "DAYS_BIRTH", "DAYS_EMPLOYED", "AMT_ANNUITY", "AMT_CREDIT", "AMT_GOODS_PRICE", "DAYS_ID_PUBLISH", "DAYS_REGISTRATION", "DAYS_LAST_PHONE_CHANGE", "AMT_INCOME_TOTAL", "OWN_CAR_AGE", "REGION_POPULATION_RELATIVE", "HOUR_APPR_PROCESS_START", "AMT_REQ_CREDIT_BUREAU_YEAR", "AMT_REQ_CREDIT_BUREAU_QRT", "DEF_30_CNT_SOCIAL_CIRCLE", "YEARS_BEGINEXPLUATATION_MODE", "TOTALAREA_MODE", "OBS_60_CNT_SOCIAL_CIRCLE", "OBS_30_CNT_SOCIAL_CIRCLE", "BASEMENTAREA_MODE", "REGION_RATING_CLIENT_W_CITY", "APARTMENTS_MODE", "LANDAREA_AVG", "BASEMENTAREA_AVG", "DEF_60_CNT_SOCIAL_CIRCLE", "CODE_GENDER", "LANDAREA_MODE", "AMT_REQ_CREDIT_BUREAU_MON", "YEARS_BEGINEXPLUATATION_MEDI", "REG_CITY_NOT_LIVE_CITY", "NONLIVINGAREA_MEDI", "LANDAREA_MEDI", "BASEMENTAREA_MEDI", "COMMONAREA_MEDI", "YEARS_BEGINEXPLUATATION_AVG", "LIVINGAREA_MEDI", "CNT_FAM_MEMBERS"]
    row = []
    for feat in features:
        row.append(req[feat])
    row = np.asarray(row)
    row = row.reshape(1, row.shape[0])
    model1 = lgb.Booster(model_file=os.path.join(app.root_path,
    'files/lgb-model-1554813671-0.txt'))
    model2 = lgb.Booster(model_file=os.path.join(app.root_path,
    'files/lgb-model-1554813671-1.txt'))
    model3 = lgb.Booster(model_file=os.path.join(app.root_path,
    'files/lgb-model-1554813671-2.txt'))
    pred1 = model1.predict(row)[0]
    pred2 = model2.predict(row)[0]
    pred3 = model3.predict(row)[0]
    prediction = (pred1 + pred2 + pred3) / 3
    return jsonify({"prediction": prediction, "p1": pred1, "p2": pred2, "p3":
        pred3})
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

