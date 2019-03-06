from app import app
from pymongo import PyMongo


db = PyMongo(app)

class User(db.Model, UserMixin):
    username = db.Column(db.Integer)
    # email = db.StringF()
    # password = db.StringField()

