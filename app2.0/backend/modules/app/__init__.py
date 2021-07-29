''' flask app with mongo '''
import os
import json
import datetime
from bson.objectid import ObjectId
from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS



class JSONEncoder(json.JSONEncoder):# extended the json-encoder class to support ObjectId & datetime data types 
    ''' extend json-encoder class'''

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, set):
            return list(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


# create the flask object
app = Flask(__name__)
cors = CORS(app)
#app.config['PROPAGATE_EXCEPTIONS'] = False
#app.config['MONGO_URI'] = os.environ.get('DB')#adding db to the app #Docker
app.config['MONGO_URI'] = 'mongodb+srv://vicky:root123@cluster0.gnmhi.mongodb.net/ATS' #adding db to the app
app.config['JWT_SECRET_KEY'] ='to-do-app-secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
app.config['UPLOADED_FILES'] = 'static/files'
if not os.path.exists('static/files'):
    os.makedirs('static/files')
mongo = PyMongo(app)
flask_bcrypt = Bcrypt(app)
jwt = JWTManager(app)
app.json_encoder = JSONEncoder

from app.controllers import *  # pylint: disable=W0401,C0413
