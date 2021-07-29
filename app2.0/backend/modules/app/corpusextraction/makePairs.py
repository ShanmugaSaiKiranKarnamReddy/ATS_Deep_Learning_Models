import json
import pymongo
import json
from json import loads
from pymongo import MongoClient
import nltk
import csv

cluster = MongoClient("mongodb+srv://vicky:root123@cluster0.gnmhi.mongodb.net/test")
db = cluster["ATS2"]
data = []
cur_cv = db.cv_corpus.find() #total 2252
cur_jd = db.jd_corpus.find() #total 51

cur_cv_list=[]
cur_jd_list=[]
for jd in cur_jd:
  cur_cv_list.append(jd)

for cv in cur_cv:
    cur_jd_list.append(cv)

for jd in cur_cv_list:
  for cv in cur_jd_list:
    print(jd['skill'], cv['skill'])


