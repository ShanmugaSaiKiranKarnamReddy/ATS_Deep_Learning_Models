import gensim
import logging
import pandas as pd
import json
import pymongo
import json
from json import loads
from pymongo import MongoClient
import os
from os.path import isfile, join
from app import app, mongo, flask_bcrypt, jwt
from .predict_bi_lstm import get_bi_lstm_result
from collections import defaultdict
from scipy.stats.mstats import gmean
import random
from bson.objectid import ObjectId
import json
import statistics

# from flask_jwt_extended import (create_access_token, create_refresh_token,
#                                 jwt_required, jwt_refresh_token_required, get_jwt_identity)

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def get_random_pair(session_id):
    cur_cv = mongo.db.cv_corpus.find({"session_id": session_id})
    cur_jd = mongo.db.jd_corpus.find({"session_id": session_id})

    cur_cv_list=[]
    cur_jd_list=[]
    test_jd_corpus = []
    test_cv_corpus = []
    pair = []
    for jd in cur_jd:
        if(jd["jd_corpus"] not in test_jd_corpus):
            test_jd_corpus.append(jd["jd_corpus"])
            cur_jd_list.append(jd)

    for cv in cur_cv:
        if(cv["cv_corpus"] not in test_cv_corpus):
            test_cv_corpus.append(cv["cv_corpus"])
            cur_cv_list.append(cv)
    for jd in cur_jd_list:
        for cv in cur_cv_list:
            pair.append({
                "Resume": cv["cv_corpus"], 
                "cv_mongo_object_id": cv["cv_mongo_object_id"], 
                "cv_session_id": cv["session_id"], 
                "JD": jd["jd_corpus"], 
                "jd_mongo_object_id": jd["jd_mongo_object_id"],
                "jd_session_id": jd["session_id"]
                })
            
    return pair



def word_2_vec(pair):
    """
    Extract questions for making word2vec model.
    """
    # cur_cv = mongo.db.cv_corpus.find({"session_id": session_id})
    # cur_jd = mongo.db.jd_corpus.find({"session_id": session_id})

    # cur_cv_list=[]
    # cur_jd_list=[]
    # pair = []
    # df2={}
    # for jd in cur_jd:
    #     cur_cv_list.append(jd)

    # for cv in cur_cv:
    #     cur_jd_list.append(cv)

    # for jd in cur_cv_list:
    #     for cv in cur_jd_list:
    #         pair.append({"Resume": cv["cv_corpus"], "JD": jd["jd_corpus"]})
    df2 = pd.DataFrame(pair)
 


    for dataset in [df2]:
        for i, row in dataset.iterrows():
            if i != 0 and i % 1000 == 0:
                logging.info("read {0} sentences".format(i))

            if row['Resume']:
                yield gensim.utils.simple_preprocess(row['Resume'])
            if row['JD']:
                yield gensim.utils.simple_preprocess(row['JD'])
    
def CountFrequency(my_list):
    threshold_5 = 20
    threshold_4 = 100
    threshold_3 = 120
    threshold_2 = 200
    threshold_1 = 400
    final_result = '0'
    # Creating an empty dictionary
    freq = {}
    for item in my_list:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1
    for key,value in freq.items():
        if (key == 5,value > threshold_5) or (key == 4, value > threshold_4):
            final_result = '5'
        elif (key == 4,value> threshold_4) or (key == 3, value > threshold_3):
            final_result = '4'
        elif (key == 3,value> threshold_3) or (key == 2, value > threshold_2):
            final_result = '3'
        elif (key == 2,value> threshold_2) or (key == 1, value > threshold_1):
            final_result = '2'
        else:
            final_result = '1'
  
    return final_result

def getUser(cv_mongo_object_id):
    cv_cur = mongo.db.cv_struct.find({"_id": ObjectId(cv_mongo_object_id)})

    filename=''
    # print(list(cv_cur))
    for cv in cv_cur:
        print(cv['file_name'])

        filename = cv['file_name']

    return filename
def normalized_score(results):
   
    tmp = defaultdict(list)

    for item in results:
        tmp[item['cv_mongo_object_id']].append(int(item['score']))

    
    return [{'filename': getUser(k), 'result':round(statistics.mean(v), 2)} for k,v in tmp.items()]

    


def final_result_bi_lstm(session_id):
    documents=[]
    random_pairs = get_random_pair(session_id)
    documents = [x for x in next(word_2_vec(random_pairs))]
    logging.info("Done reading data file")

    model = gensim.models.Word2Vec(documents, size=300)
    model.train(documents, total_examples=len(documents), epochs=50)
    model.save(os.path.join(__location__, 'Resume_JD_new_14.w2v'))
    result = get_bi_lstm_result(random_pairs)
    
    return normalized_score(result)

