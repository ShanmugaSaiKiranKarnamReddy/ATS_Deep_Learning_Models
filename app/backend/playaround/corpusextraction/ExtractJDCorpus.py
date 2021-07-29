from PIL import Image
import json
import pymongo
import json
from json import loads
from pymongo import MongoClient
import re

cluster = MongoClient("mongodb+srv://vicky:root123@cluster0.gnmhi.mongodb.net/test")
db = cluster["ATS"]

local_cluster = MongoClient("localhost:27017")
local_db = local_cluster["ATS"]
local_collection_jd_struct = local_db["jd_struct"]
local_jd_corpus = local_db["jd_corpuses"]
cv_corpus = db["jd_corpuses"]


        

for mainIndex, jd in enumerate(local_collection_jd_struct.find()):
  if jd["skills"] is not None:
    for index, skill in enumerate(jd["skills"]):
      if skill is not None:
        regexPart1 = r"([^.]*?"
        regexPart2 = r"[^.]*\.)"
        data = {}
        texts  = jd["all_text"].rstrip()
        print(texts)
        result = re.findall(regexPart1 + re.escape(skill) + regexPart2, texts)
        if result:
          data["jd_corpus"] = result[0].rstrip()
          data["skill"] = skill
          cv_corpus.insert_one(data)





  