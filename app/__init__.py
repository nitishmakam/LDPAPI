from flask import Flask

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/loandefault"
app.config['SECRET_KEY'] = 'secretkey'

from .models import *
from routes import *