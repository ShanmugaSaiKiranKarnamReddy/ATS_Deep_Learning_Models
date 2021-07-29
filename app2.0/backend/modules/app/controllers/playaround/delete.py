import pymongo
import json
from json import loads
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://vicky:root123@cluster0.gnmhi.mongodb.net/test")
db = cluster["ATS2.0"]

cur = mongo.db.cv_struct.find({'session_id': '1541e4e3-264b-4a1c-b0ca-cwevv'})
bulk = db.i