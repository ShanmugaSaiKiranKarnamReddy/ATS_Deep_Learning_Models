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

cur = db.cv_struct.find()
coll = []
for mainIndex, cv in enumerate(cur):
  for corpus in tokenizer.tokenize(cv["all_text"]):
    for skill in cv["skills"]:
      if skill in corpus:
        data = {}
        data["skill"] = skill
        data["cv_corpus"] = corpus
        data["cv_mongo_object_id"] = cv['_id']
        data["session_id"] = cv['session_id']
        db.cv_corpus.insert_one(data)



# for mainIndex, resume in enumerate(collection_cv_struct):
#   if resume["skills"] is not None:
#     for index, skill in enumerate(resume["skills"]):
#       if skill is not None:
#         regexPart1 = r"([^.]*?"
#         regexPart2 = r"[^.]*\.)"
#         data = {}
#         texts  = resume["all_text"].rstrip()
#         #print(texts)
#         result = re.findall(regexPart1 + re.escape(skill) + regexPart2, texts)
#         if result:
#           data["cv_corpus"] = result[0].rstrip()
#           data["skill"] = skill
#           cv_corpus.insert_one(data)  