import pymongo
import json
from json import loads
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://vicky:root123@cluster0.gnmhi.mongodb.net/test")
db = cluster["ATS"]

db["cv_struct"].remove()
db["cv_unstruct"].remove()
db["jd_struct"].remove()
db["jd_unstruct"].remove()
db["cv_corpuses"].remove()
db["jd_corpuses"].remove()