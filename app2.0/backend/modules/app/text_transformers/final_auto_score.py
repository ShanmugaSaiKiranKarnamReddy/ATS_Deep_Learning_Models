import pandas as pd
import scipy
import numpy as np
import os, sys,re
from sentence_transformers import models, SentenceTransformer
import nltk
from nltk.corpus import stopwords
import spacy
import nltk
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
nlp = spacy.load('en_core_web_sm')
from app import app, mongo, flask_bcrypt, jwt
from bson.objectid import ObjectId
from collections import defaultdict
import statistics
import math


def cleanAndSplitText(text, lema=True, removeSmall=True):
    # text = re.sub('[^A-Za-z]+', ' ', text)
    text = re.sub('[^a-zA-Z0-9äöüÄÖÜß]+', ' ', text)
    if removeSmall:
        text = re.sub(r'\W*\b\w{1,3}\b', '', text)
    text = text.lower()
    tmpWords = re.findall('\w+', text)
    # re.findall(r'[^\W\d_]+', text)
    words = []
    for word in tmpWords:
        if word not in stop_words:
            words.append(word)
    if lema:
        # lemma = nltk.wordnet.WordNetLemmatizer()
        # words = list(map(lemma.lemmatize, words))
        doc = nlp(' '.join(words))
        words = ' '.join([x.lemma_ for x in doc])
    else:
        words = ' '.join(words)
    # ps = nltk.stem.PorterStemmer()
    # words = map(ps.stem, words)
    return words

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
                "JD": jd["jd_corpus"], 
                "jd_mongo_object_id": jd["jd_mongo_object_id"],
                "jd_session_id": jd["session_id"]
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

def getUser(cv_mongo_object_id):
    cv_cur = mongo.db.cv_struct.find({"_id": ObjectId(cv_mongo_object_id)})

    filename=''
    # print(list(cv_cur))
    for cv in cv_cur:

        filename = cv['file_name']

    return filename
    
def normalized_score(results):
    tmp = defaultdict(list)
    for item in results:
      if not math.isnan(item[6]):
        if item[6] > 2:
          tmp[item[1]].append(int(item[6]))



    return [{'filename':getUser(k), 'result':round(statistics.mean(v)*20, 2) + 20, 'test': v} for k,v in tmp.items()]

def final_result_text_transformers(session_id):
  pair = get_random_pair(session_id)
  model = SentenceTransformer('T-Systems-onsite/cross-en-de-roberta-sentence-transformer')


  train_df = pd.DataFrame(pair["pair"])

  resume = list(train_df['Resume'])
  corpus = resume

  #remove nan values
  corpus = [x for x in corpus if str(x) != 'nan']

  refined_corpus = []
  for sample in corpus:
    refined_sample = cleanAndSplitText(sample, lema=False, removeSmall=True)
    refined_corpus.append(refined_sample)

  corpus_embeddings = model.encode(refined_corpus)
  #remove duplicates
  # corpus = list(dict.fromkeys(corpus))
  # corpus_embeddings = model.encode(corpus)
  #Get attribute target information
  JD = list(train_df['JD'])

  #remove nan values
  JD = [x for x in JD if str(x) != 'nan']

  refined_JD = []
  for sample in JD:
    refined_sample = cleanAndSplitText(sample, lema=False, removeSmall=True)
    refined_JD.append(refined_sample)

  JD_embeddings = model.encode(refined_JD)


  distances=[]
  for i in range(len(JD_embeddings)):
    score = scipy.spatial.distance.cdist([corpus_embeddings[i]], [JD_embeddings[i]], "cosine")[0]
    results = zip(range(len(score)), score)
    results = sorted(results, key=lambda x: x[1])
    refined_result = round(results[0][1],1)
    #score normalization
    lower, upper = 1,5
    score_norm = lower + (upper - lower) * refined_result
    if 1 <= score_norm < 2:
      distances.append(5)
    elif 2 <= score_norm < 3:
      distances.append(4)
    elif 3 <= score_norm < 3.5:
      distances.append(3)
    elif 3.5 <= score_norm < 4.5:
      distances.append(2)
    elif 4.5 <= score_norm <= 5:
      distances.append(1)
  df = pd.DataFrame(distances)
  train_df['Score'] =df

  
  # print(train_df.values.tolist())
  test = normalized_score(train_df.values.tolist())

  return test
  