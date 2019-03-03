from flask import Blueprint
from flask_jwt import JWT, jwt_required

routes = Blueprint("routes", __name__)

from .users import *

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = request.args.get("token")

#         if not token:
#             return jsonify({"message": "Token is missing!"})  # 403 error

#         try:
#             data = jwt.decode(token, app.config["SECRET_KEY"])
#         except:
#             return jsonify({"message": "Token is invalid!"})  # 403 error

#         return f(*args, **kwargs)

#     return decorated
