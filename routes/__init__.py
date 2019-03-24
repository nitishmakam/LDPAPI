from flask import Blueprint
from app import app

from .users import users
from .predictions import prediction

app.register_blueprint(users)
app.register_blueprint(prediction)

@app.route('/')
def index():
    return "Hey,there!"
