import pymongo
import json
from json import loads
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://vicky:root123@cluster0.gnmhi.mongodb.net/test")
db = cluster["ATS"]

db["jd_corpuses"].remove()
