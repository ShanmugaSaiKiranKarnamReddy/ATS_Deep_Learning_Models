import json
import pymongo
import json
from json import loads
from pymongo import MongoClient
import nltk
import csv

cluster = MongoClient("mongodb+srv://vicky:root123@cluster0.gnmhi.mongodb.net/test")
db = cluster["ATS"]

local_cluster = MongoClient("localhost:27017")
local_db = local_cluster["ATS"]
local_collection_cv_struct = local_db["cv_struct"]
collection_cv_struct = db["cv_struct"].find()
local_cv_corpus = local_db["cv_corpuses"]
cv_corpuses = db["cv_corpuses"].find()
jd_corpuses = db["jd_corpuses"].find()
corpus_pairs = db["corpus_pairs"]

data = []

# for cv_corpus in cv_corpuses:
#   #print(cv_corpus)
#   for jd_corpus in jd_corpuses:
#     data.append({jd_corpus["jd_corpus"],cv_corpus["cv_corpus"]})

x = 0
type(cv_corpuses)
for jd_corpus in jd_corpuses:
  for cv_corpus in cv_corpuses:
    x +=1

    #data.append(jd_corpus["jd_corpus"],cv_corpus["cv_corpus"])


print(x)
# with open('test.csv', 'w', newline="") as outf:
#     dw = csv.writer(outf)
#     #dw.writeheader(["jd_sentence", jd_skill, cv_sentence, cv_skill])
#     for row in data:
#         dw.writerow(row)