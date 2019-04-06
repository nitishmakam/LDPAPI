from flask import Blueprint, request, make_response, jsonify
from flask_bcrypt import bcrypt
import jwt
from app import app
from datetime import datetime, timedelta
from app.token_required import token_required
users = Blueprint("users", __name__, url_prefix="/users")
from app import mydb

user = mydb["User"]


@users.route("/usernameExists/<username>", methods=['GET'])
def check(username=None):
    request.args.get('username', username)
    existing_users = user.find({"username": username})
    if (not existing_users.count()):
        return ("", 200)
    else:
        error = {'message': 'Username not available'}
        return jsonify(error), 409


@users.route("/register", methods=['POST'])
def add_user():
    print(request.json)
    email = request.json['email']
    existing_users = user.find({'email': email})
    if (existing_users.count()):
        error = {'message': 'An account already exists with this email id.'}
        return jsonify(error), 409
    username = request.json['username']
    password = request.json['password']
    obj = {'username': username, 'email': email, 'password': password}
    user.insert(obj)
    return "", 200


@users.route("/login", methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    # print(username, password)
    existing_users = user.find(
        {"$and": [{
            'username': username
        }, {
            'password': password
        }]})
    if (existing_users.count()):
        
        token = jwt.encode({
            'username': username,
            'exp': datetime.utcnow() + timedelta(seconds=3000)
        }, app.config.get('SECRET_KEY'))
        response = {'token': token.decode('UTF-8')}
        print(response)
        return jsonify(response), 200
    else:
        return "", 403
