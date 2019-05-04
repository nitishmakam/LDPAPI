from flask import Blueprint,render_template
from app import app

from .users import users
from .predictions import prediction

app.register_blueprint(users)
app.register_blueprint(prediction)

@app.route('/')
def index():
    return render_template("index.html")

    
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
