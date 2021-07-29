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
from .predict_model import predict_model
from collections import defaultdict
from scipy.stats.mstats import gmean
import random
from bson.objectid import ObjectId
import json
import statistics
from ..knowledge_graph import get_kg_scores

# from flask_jwt_extended import (create_access_token, create_refresh_token,
#                                 jwt_required, jwt_refresh_token_required, get_jwt_identity)

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

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


    cur_cv_list_skills=[]
    cur_jd_list_skills=[]
    test_jd_skills = []
    test_cv_skills = []
    skills_pair = []


    for jd in cur_jd:
        if(jd["jd_corpus"] not in test_jd_corpus):
            test_jd_corpus.append(jd["jd_corpus"])
            cur_jd_list.append(jd)
        if(jd["skill"] not in test_jd_skills):
            test_jd_skills.append(jd["skill"])
            cur_jd_list_skills.append(jd)

    for cv in cur_cv:
        if(cv["cv_corpus"] not in test_cv_corpus):
            test_cv_corpus.append(cv["cv_corpus"])
            cur_cv_list.append(cv)
        if({cv["skill"], cv["cv_mongo_object_id"]} not in test_cv_skills):
            test_cv_skills.append({cv["skill"], cv["cv_mongo_object_id"]})
            cur_cv_list_skills.append(cv)

    for jd in cur_jd_list:
        for cv in cur_cv_list:
            pair.append({
                "Resume": cv["cv_corpus"], 
                "cv_mongo_object_id": cv["cv_mongo_object_id"], 
                "cv_session_id": cv["session_id"], 
                "cv_corpus_skill":cv["skill"],
                "JD": jd["jd_corpus"], 
                "jd_mongo_object_id": jd["jd_mongo_object_id"],
                "jd_session_id": jd["session_id"],
                "jd_corpus_skill": jd["skill"]
                })

    for jd in cur_jd_list_skills:
        for cv in cur_cv_list_skills:
            skills_pair.append({ 
                "cv_corpus_skill":cv["skill"],
                "cv_mongo_object_id": cv["cv_mongo_object_id"], 
                "cv_session_id": cv["session_id"], 
                "jd_corpus_skill": jd["skill"],
                "jd_mongo_object_id": jd["jd_mongo_object_id"],
                "jd_session_id": jd["session_id"],
                })
  
    
    return {"pair": pair, "skills_pair": skills_pair}



def word_2_vec(pair):
    """
    Extract questions for making word2vec model.
    """

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

        filename = cv['file_name']

    return filename

def threshold_kg_score(scores):
    threshold_ = 3
    num_ = 0 #number of genuine result
    sum_ = 0
    for score in scores:
        if score > 0:
            num_ +=1
            sum_ +=score
    
    if num_ != 0:
        if threshold_ < num_ < 5:# atleast more matches than a threshold from kg
            avg_ = sum_/num_
            return avg_*12
        elif 5 < num_ < 7:
            avg_ = sum_/num_
            return avg_*15
        elif 7 < num_ < 9:
            avg_ = sum_/num_
            return avg_*18
        elif 7 < num_:
            avg_ = sum_/num_
            return avg_*20
        else:
            return 0
    else:
        return 0

def normalized_kg_score(kg_results):
    tmp_kg_result = defaultdict(list)
    for item in kg_results:
        print(getUser(item['cv_mongo_object_id']), int(item['kg_score']), "also here")
    
    # print(kg_results, "lolp")
    for item in kg_results:
        tmp_kg_result[item['cv_mongo_object_id']].append(int(item['kg_score']))
    
    for k, v in tmp_kg_result.items():
        print(getUser(k),v, "here")
        
    return [{'filename':getUser(k), 'result':round(threshold_kg_score(v), 2), 'test': v } for k,v in tmp_kg_result.items()]



def normalized_model_score(results):
    tmp = defaultdict(list)
    
    for item in results:
        tmp[item['cv_mongo_object_id']].append(int(item['score']))


    # return [{'filename':getUser(k), 'result':combine_score(v, kg_results), 'test': v } for k,v in tmp.items()]
    return [{'filename':getUser(k), 'result':round(statistics.mean(v), 2), 'test': v } for k,v in tmp.items()]

def combined_score(normalized_kg_score, normalized_model_score):
    result= []
    for model_score in normalized_model_score:
        for kg_score in normalized_kg_score:
            if model_score["filename"] == kg_score["filename"]:
                result.append({
                    "filename": model_score["filename"],
                    "result": round(statistics.mean([model_score["result"], kg_score["result"]]) + 20, 2)
                })
    return result


def final_result_siamese_lstm(session_id):
    documents=[]
    random_pairs = get_random_pair(session_id)       

    documents = [x for x in next(word_2_vec(random_pairs["pair"]))]
    logging.info("Done reading data file")

    model = gensim.models.Word2Vec(documents, size=300)
    model.train(documents, total_examples=len(documents), epochs=50)
    model.save(os.path.join(__location__, 'Resume_JD_new_14.w2v'))
    kg_results = get_kg_scores(random_pairs["skills_pair"])
    result = predict_model(random_pairs["pair"])
    normalized_model_score_result = normalized_model_score(result)
    normalized_kg_score_result = normalized_kg_score(kg_results)
    combined_score_result = combined_score(normalized_kg_score_result, normalized_model_score_result)
    
    return combined_score_result

