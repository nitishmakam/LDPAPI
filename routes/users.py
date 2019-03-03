from . import routes
from flask_jwt import jwt_required


@routes.route("/users")
@jwt_required()
def index():
    return "Hello,Users!"

