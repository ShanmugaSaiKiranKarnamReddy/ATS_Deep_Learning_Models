

import json
import pymongo
import json
from json import loads
from pymongo import MongoClient

local_cluster = MongoClient("localhost:27017")
local_db = local_cluster["ATS"]
local_jd_corpus = local_db["jd_corpus"]
local_cv_corpuses = local_db["cv_corpuses"]
local_cv_pairs = local_db["pairs"]


# duplicate_corpus = None
# for corpus in enumerate(local_cv_corpuses.find()):
#   if duplicate_corpus:
#   print(corpus)


local_cv_corpuses.ensure_index({ "cv_corpus" : 1}, {"unique":True, "dropDups" : True})

 