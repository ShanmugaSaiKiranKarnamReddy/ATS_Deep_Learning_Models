
from neo4j import GraphDatabase, basic_auth
from csv import reader, writer
import os
from os.path import isfile, join
from pymongo import MongoClient
from app import app, mongo, flask_bcrypt, jwt
driver = GraphDatabase.driver("bolt://localhost:7687", auth= basic_auth(user = "neo4j", password = "password"))
from bson.objectid import ObjectId

def find_node(tx, name):
    levels = []
    names = []
    result = tx.run("MATCH (a)"
                    "WHERE a.name = $name "
                    "RETURN a.level AS level, a.name AS name", name=name)
    for record in result:
        levels.append(record["level"])
        names.append(record["name"])
    return levels, names


def find_relation(tx, row):
    relation1 = []
    relation2 = []
    result1 = tx.run("Match (n)-[]->(m)"
                     "Where m.name= $JDword and n.name = $CVword "
                     "Return m.name AS name", JDword = row["jd_corpus_skill"], CVword =row["cv_corpus_skill"])
    result2 = tx.run("Match (m)-[]->(n)"
                     "Where m.name= $JDword and n.name = $CVword "
                     "Return m.name AS name", JDword = row["jd_corpus_skill"], CVword =row["cv_corpus_skill"])
    for record in result1:
        relation1.append(record["name"])
    for record in result2:
        relation2.append(record["name"])
    return relation1, relation2

def getUser(cv_mongo_object_id):
    cv_cur = mongo.db.cv_struct.find({"_id": ObjectId(cv_mongo_object_id)})

    filename=''
    # print(list(cv_cur))
    for cv in cv_cur:

        filename = cv['file_name']

    return filename

def get_kg_scores(pairs):
    result = []
    print(pairs, "lol")
    for index, row in enumerate(pairs):
        if row["jd_corpus_skill"] is None or row["cv_corpus_skill"] is None:
            row["jd_corpus_skill"] = ""
            row["cv_corpus_skill"] = ""
        
        row["jd_corpus_skill"] = str(row["jd_corpus_skill"]).lower()
        row["cv_corpus_skill"] = str(row["cv_corpus_skill"]).lower()
        
        
        
        
        with driver.session() as session:
            jd_level, jd_name = session.read_transaction(find_node, row["jd_corpus_skill"])
            cv_level, cv_name = session.read_transaction(find_node, row["cv_corpus_skill"])
            relation_result1, relation_result2 = session.read_transaction(find_relation, row)

            if jd_name == [] or cv_name == []:
                score = 0
                result.append({
                                "cv_corpus_skill":row["cv_corpus_skill"],
                                "cv_mongo_object_id": row["cv_mongo_object_id"], 
                                "cv_session_id": row["cv_session_id"], 
                                "jd_corpus_skill": row["jd_corpus_skill"],
                                "jd_mongo_object_id": row["jd_mongo_object_id"],
                                "jd_session_id": row["jd_session_id"],
                                "kg_score": score
                            })

            elif jd_name == cv_name:
                score = 5
                result.append({
                                "cv_corpus_skill":row["cv_corpus_skill"],
                                "cv_mongo_object_id": row["cv_mongo_object_id"], 
                                "cv_session_id": row["cv_session_id"], 
                                "jd_corpus_skill": row["jd_corpus_skill"],
                                "jd_mongo_object_id": row["jd_mongo_object_id"],
                                "jd_session_id": row["jd_session_id"],
                                "kg_score": score
                            })

            else:
                for c in relation_result1:
                    res = isinstance(c, str)
                    if res == True:
                        print("relation exists, node= ", c)
                        if jd_level < cv_level:
                            score = 4
                            result.append({
                                "cv_corpus_skill":row["cv_corpus_skill"],
                                "cv_mongo_object_id": row["cv_mongo_object_id"], 
                                "cv_session_id": row["cv_session_id"], 
                                "jd_corpus_skill": row["jd_corpus_skill"],
                                "jd_mongo_object_id": row["jd_mongo_object_id"],
                                "jd_session_id": row["jd_session_id"],
                                "kg_score": score
                            })
                        elif cv_level < jd_level:
                            score = 3
                            result.append({
                                "cv_corpus_skill":row["cv_corpus_skill"],
                                "cv_mongo_object_id": row["cv_mongo_object_id"], 
                                "cv_session_id": row["cv_session_id"], 
                                "jd_corpus_skill": row["jd_corpus_skill"],
                                "jd_mongo_object_id": row["jd_mongo_object_id"],
                                "jd_session_id": row["jd_session_id"],
                                "kg_score": score
                            })
                for c in relation_result2:
                    res = isinstance(c, str)
                    if res == True:
                        print("relation exists, node= ", c)
                        if jd_level < cv_level:
                            score = 4
                            result.append({
                                "cv_corpus_skill":row["cv_corpus_skill"],
                                "cv_mongo_object_id": row["cv_mongo_object_id"], 
                                "cv_session_id": row["cv_session_id"], 
                                "jd_corpus_skill": row["jd_corpus_skill"],
                                "jd_mongo_object_id": row["jd_mongo_object_id"],
                                "jd_session_id": row["jd_session_id"],
                                "kg_score": score
                            })
                        elif cv_level < jd_level:
                            score = 3
                            result.append({
                                "cv_corpus_skill":row["cv_corpus_skill"],
                                "cv_mongo_object_id": row["cv_mongo_object_id"], 
                                "cv_session_id": row["cv_session_id"], 
                                "jd_corpus_skill": row["jd_corpus_skill"],
                                "jd_mongo_object_id": row["jd_mongo_object_id"],
                                "jd_session_id": row["jd_session_id"],
                                "kg_score": score
                            })
        driver.close()


    # pair_unique = []
    # result_list = []
    for score in result:
        print(score["cv_corpus_skill"], score["jd_corpus_skill"],score["kg_score"],  getUser(score["cv_mongo_object_id"]),"check")
    # print(result, "done")
    return result

