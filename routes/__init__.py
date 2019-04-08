<<<<<<< HEAD
from flask import Blueprint,render_template
from flask_jwt import JWT, jwt_required
=======
from flask import Blueprint
>>>>>>> 9568d7321e64eae58ba08e78216ef5e515b3f094
from app import app

from .users import users
from .predictions import prediction

app.register_blueprint(users)
app.register_blueprint(prediction)

@app.route('/')
def index():
<<<<<<< HEAD
    return "Hello"

    
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get("token")

        if not token:
            return jsonify({"message": "Token is missing!"})  # 403 error

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
        except:
            return jsonify({"message": "Token is invalid!"})  # 403 error

        return f(*args, **kwargs)

    return decorated
=======
    return "Hey,there!"
>>>>>>> 9568d7321e64eae58ba08e78216ef5e515b3f094
