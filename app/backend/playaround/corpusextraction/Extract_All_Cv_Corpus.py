from PIL import Image
import json
import pymongo
import json
from json import loads
from bson.objectid import ObjectId
from pymongo import MongoClient
import re

cluster = MongoClient("mongodb+srv://vicky:root123@cluster0.gnmhi.mongodb.net/test")
db = cluster["ATS"]

local_cluster = MongoClient("localhost:27017")
local_db = local_cluster["ATS"]
local_collection_cv_struct = local_db["cv_struct"]
collection_cv_struct = db["cv_struct"].find()
local_cv_corpus = local_db["cv_corpuses"]
cv_corpus = db["cv_corpuses"]



for mainIndex, resume in enumerate(collection_cv_struct):
  if resume["skills"] is not None:
    for index, skill in enumerate(resume["skills"]):
      if skill is not None:
        regexPart1 = r"([^.]*?"
        regexPart2 = r"[^.]*\.)"
        data = {}
        texts  = resume["all_text"].rstrip()
        #print(texts)
        result = re.findall(regexPart1 + re.escape(skill) + regexPart2, texts)
        if result:
          data["cv_corpus"] = result[0].rstrip()
          data["skill"] = skill
          cv_corpus.insert_one(data)  