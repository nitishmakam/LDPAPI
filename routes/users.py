from flask import Blueprint,request,make_response
# from flask_bcrypt import bcrypt
from flask_jwt import jwt_required
from app import app
from app.token_required import token_required
from app.models import *
users = Blueprint("users", __name__, url_prefix="/users")

user=User(username="nitish",email="a",password="b")
user.save()

@users.route("/register/usernameExists/<username>",methods=['GET'])
def register(username=None):
    request.args.get('username',username)
    existing_users = User.query.filter({User.username:username}).first()
    if(existing_users==None):
        return "Hello,"+username
    else:
        return make_response("Username is already taken",409)