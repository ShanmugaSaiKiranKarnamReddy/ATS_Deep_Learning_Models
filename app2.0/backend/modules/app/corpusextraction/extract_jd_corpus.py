from PIL import Image
import json
import pymongo
import json
from json import loads
from bson.objectid import ObjectId
from pymongo import MongoClient
import re

import nltk
nltk.download('punkt')

from app import app, mongo, flask_bcrypt, jwt
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
import nltk.data

#tokenizer = nltk.data.load('tokenizers/punkt/english.pickle'

def extract_jd_corpus(session_id):
  cur = mongo.db.jd_struct.find({'session_id': session_id})
  for mainIndex, jd in enumerate(cur):
    for corpus in nltk.sent_tokenize(jd["all_text"]):
      for skill in jd["skills"]:
        if skill in corpus:
          data = {}
          data["skill"] = skill
          data["expericene"] = None
          data["degree"] = None
          data["designation"] = None
          data["college_name"] = None
          data["company_names"] = None
          data["jd_corpus"] = corpus
          data["jd_mongo_object_id"] = jd['_id']
          data["session_id"] = jd['session_id']
          mongo.db.jd_corpus.insert_one(data)

      if jd["experience"] is not None:
        for experience in jd["experience"]:
          data = {}
          data["skill"] = None
          data["expericene"] = experience
          data["degree"] = None
          data["designation"] = None
          data["college_name"] = None
          data["company_names"] = None
          data["jd_corpus"] = experience
          data["jd_mongo_object_id"] = jd['_id']
          data["session_id"] = jd['session_id']
          mongo.db.jd_corpus.insert_one(data)
          
      if jd["degree"] is not None:
        for degree in jd["degree"]:
          data = {}
          data["skill"] = None
          data["expericene"] =  None
          data["degree"] = degree
          data["designation"] = None
          data["college_name"] = None
          data["company_names"] = None
          data["jd_corpus"] = degree
          data["jd_mongo_object_id"] = jd['_id']
          data["session_id"] = jd['session_id']

      if jd["designation"] is not None:
        for designation in jd["designation"]:
          data = {}
          data["skill"] = None
          data["expericene"] =  None
          data["degree"] = None
          data["designation"] = designation
          data["college_name"] = None
          data["company_names"] = None
          data["jd_corpus"] = designation
          data["jd_mongo_object_id"] = jd['_id']
          data["session_id"] = jd['session_id']
          mongo.db.jd_corpus.insert_one(data)


      if jd["college_name"] is not None:
        for college_name in jd["college_name"]:
          data = {}
          data["skill"] = None
          data["expericene"] = None
          data["degree"] = None
          data["designation"] = None
          data["college_name"] = college_name
          data["company_names"] = None
          data["jd_corpus"] = college_name
          data["jd_mongo_object_id"] = jd['_id']
          data["session_id"] = jd['session_id']
          mongo.db.jd_corpus.insert_one(data)


      if jd["company_names"] is not None:
        for company_names in jd["company_names"]:
          data = {}
          data["skill"] = None
          data["expericene"] = None
          data["degree"] = None
          data["designation"] = None
          data["college_name"] = None
          data["company_names"] = company_names
          data["jd_corpus"] = company_names
          data["jd_mongo_object_id"] = jd['_id']
          data["session_id"] = jd['session_id']
          mongo.db.jd_corpus.insert_one(data)