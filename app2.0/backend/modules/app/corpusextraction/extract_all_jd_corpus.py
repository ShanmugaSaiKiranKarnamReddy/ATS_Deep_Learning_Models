from PIL import Image
import json
import pymongo
import json
from json import loads
from pymongo import MongoClient
import re
# from app import app, mongo, flask_bcrypt, jwt
# from flask_jwt_extended import (create_access_token, create_refresh_token,
#                                 jwt_required, jwt_refresh_token_required, get_jwt_identity)
import nltk.data

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

cluster = MongoClient("mongodb+srv://vicky:root123@cluster0.gnmhi.mongodb.net/test")
db = cluster["ATS2"]

cur = db.jd_struct.find()
coll = []
for mainIndex, jd in enumerate(cur):
  for corpus in tokenizer.tokenize(jd["all_text"]):
    for skill in jd["skills"]:
      if skill in corpus:
        data = {}
        data["skill"] = skill
        data["jd_corpus"] = corpus
        data["jd_mongo_object_id"] = jd['_id']
        data["session_id"] = jd['session_id']
        db.jd_corpus.insert_one(data)
  # if jd["skills"] is not None:
  #   for index, skill in enumerate(jd["skills"]):
  #     if skill is not None:
  #       regexPart1 = r"([^.]*?"
  #       regexPart2 = r"[^.]*\.)"
  #       data = {}
  #       texts  = jd["all_text"].rstrip()
  #       result = re.findall(regexPart1 + re.escape(skill) + regexPart2, texts)
  #       if result:
  #         data["jd_corpus"] = result[0].rstrip()
  #         data["skill"] = skill
  #         for doc in cur:
  #           print(doc['_id'])
  #           data["jd_mongo_id"] = doc['_id']
  #         print(data)
  #         db.jd_corpus.insert_one(data)

