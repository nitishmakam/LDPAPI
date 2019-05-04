from flask import Flask
from flask_cors import CORS
import pymongo


app = Flask(__name__,template_folder="templates",static_folder="static")
CORS(app)
my_client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
mydb = my_client["ldp"]
app.config['SECRET_KEY'] = 'secretkey'

from routes import *
