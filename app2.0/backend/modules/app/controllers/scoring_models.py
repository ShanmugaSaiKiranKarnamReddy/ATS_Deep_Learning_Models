''' controller and routes for scoring models '''
import os
import pathlib
from flask import request, jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from app import app, mongo, flask_bcrypt, jwt
from app.schemas import validate_user
import logger
import json
from werkzeug.utils import secure_filename

from ..textextraction import jd_extraction
from ..textextraction import cv_extraction

from ..keywordmatching import final_result_keyword_matching
from ..tfidf import final_result_tfidf
from ..siamese_manhattan_lstm import final_result_siamese_lstm
from ..RNN import final_result_rnn
from ..bi_lstm import final_result_bi_lstm
from ..text_transformers import final_result_text_transformers
import uuid

@app.route('/result_keywordmatching', methods = ['GET', 'POST'])
@jwt_required
def result_keywordmatching():
   if request.method == 'POST':
     if request.files:
        uploaded_files_jd = request.files.getlist("jd")
        uploaded_files_cv = request.files.getlist("cv")
        session_id = request.values.get('session_id')
        user = get_jwt_identity()

        mongo_session  = mongo.db.sessions.find_one({"session_id": session_id})


        if mongo_session is None:
          os.makedirs(app.config['UPLOADED_FILES'] + "/" + user["email"]+ "/" + session_id + "/" + "jd")#create folder
          os.makedirs(app.config['UPLOADED_FILES'] + "/" + user["email"]+ "/" + session_id + "/" + "cv")#create folder

          for file in uploaded_files_jd:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOADED_FILES'], user["email"], session_id, "jd" ,filename))
          
          for file in uploaded_files_cv:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOADED_FILES'], user["email"], session_id, "cv" ,filename))
          
          #TEXT EXTRACTION AND CORPUS CREATION
          jd_extraction(session_id)
          cv_extraction(session_id)


        result = final_result_keyword_matching(session_id)
        mongo.db.sessions.insert_one({'session_id': session_id})

        #test.communicate()[0]
        return jsonify({'ok': True, 'data': result}), 200

@app.route('/result_tfidf', methods = ['GET', 'POST'])
@jwt_required
def result_tfidf():
   if request.method == 'POST':
     if request.files:
        uploaded_files_jd = request.files.getlist("jd")
        uploaded_files_cv = request.files.getlist("cv")
        session_id = request.values.get('session_id')
        user = get_jwt_identity()
        mongo_session  = mongo.db.sessions.find_one({"session_id": session_id})


        if mongo_session is None:
          os.makedirs(app.config['UPLOADED_FILES'] + "/" + user["email"]+ "/" + session_id + "/" + "jd")#create folder
          os.makedirs(app.config['UPLOADED_FILES'] + "/" + user["email"]+ "/" + session_id + "/" + "cv")#create folder

          for file in uploaded_files_jd:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOADED_FILES'], user["email"], session_id, "jd" ,filename))
          
          for file in uploaded_files_cv:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOADED_FILES'], user["email"], session_id, "cv" ,filename))
          
          #TEXT EXTRACTION AND CORPUS CREATION
          jd_extraction(session_id)
          cv_extraction(session_id)


        result = final_result_tfidf(session_id)
        mongo.db.sessions.insert_one({'session_id': session_id})

        #test.communicate()[0]
        return jsonify({'ok': True, 'data': result}), 200


@app.route('/result_malstm', methods = ['GET', 'POST'])
@jwt_required
def result_malstm():
   if request.method == 'POST':
     if request.files:
        uploaded_files_jd = request.files.getlist("jd")
        uploaded_files_cv = request.files.getlist("cv")
        session_id = request.values.get('session_id')
        user = get_jwt_identity()
        mongo_session  = mongo.db.sessions.find_one({"session_id": session_id})


        if mongo_session is None:

          os.makedirs(app.config['UPLOADED_FILES'] + "/" + user["email"]+ "/" + session_id + "/" + "jd")#create folder
          os.makedirs(app.config['UPLOADED_FILES'] + "/" + user["email"]+ "/" + session_id + "/" + "cv")#create folder

          for file in uploaded_files_jd:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOADED_FILES'], user["email"], session_id, "jd" ,filename))
          
          for file in uploaded_files_cv:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOADED_FILES'], user["email"], session_id, "cv" ,filename))
          
          #TEXT EXTRACTION AND CORPUS CREATION
          jd_extraction(session_id)
          cv_extraction(session_id)


        result = final_result_siamese_lstm(session_id)#this gets the final result, define a good fn name
        mongo.db.sessions.insert_one({'session_id': session_id})
        
        return jsonify({'ok': True, 'data': result}), 200
        

@app.route('/result_rnn', methods = ['GET', 'POST'])
@jwt_required
def result_rnn():
   if request.method == 'POST':
     if request.files:
        uploaded_files_jd = request.files.getlist("jd")
        uploaded_files_cv = request.files.getlist("cv")
        session_id = request.values.get('session_id')
        user = get_jwt_identity()
        mongo_session  = mongo.db.sessions.find_one({"session_id": session_id})


        if mongo_session is None:
          os.makedirs(app.config['UPLOADED_FILES'] + "/" + user["email"]+ "/" + session_id + "/" + "jd")#create folder
          os.makedirs(app.config['UPLOADED_FILES'] + "/" + user["email"]+ "/" + session_id + "/" + "cv")#create folder

          for file in uploaded_files_jd:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOADED_FILES'], user["email"], session_id, "jd" ,filename))
          
          for file in uploaded_files_cv:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOADED_FILES'], user["email"], session_id, "cv" ,filename))
          
          #TEXT EXTRACTION AND CORPUS CREATION
          jd_extraction(session_id)
          cv_extraction(session_id)


        result = final_result_rnn(session_id)#this gets the final result, define a good fn name
        mongo.db.sessions.insert_one({'session_id': session_id})
        return jsonify({'ok': True, 'data': result}), 200

@app.route('/result_bi_lstm', methods = ['GET', 'POST'])
@jwt_required
def result_bi_lstm():
   if request.method == 'POST':
     if request.files:
        uploaded_files_jd = request.files.getlist("jd")
        uploaded_files_cv = request.files.getlist("cv")
        session_id = request.values.get('session_id')
        user = get_jwt_identity()

        mongo_session  = mongo.db.sessions.find_one({"session_id": session_id})


        if mongo_session is None:
          os.makedirs(app.config['UPLOADED_FILES'] + "/" + user["email"]+ "/" + session_id + "/" + "jd")#create folder
          os.makedirs(app.config['UPLOADED_FILES'] + "/" + user["email"]+ "/" + session_id + "/" + "cv")#create folder

          for file in uploaded_files_jd:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOADED_FILES'], user["email"], session_id, "jd" ,filename))
          
          for file in uploaded_files_cv:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOADED_FILES'], user["email"], session_id, "cv" ,filename))
          
          #TEXT EXTRACTION AND CORPUS CREATION
          jd_extraction(session_id)
          cv_extraction(session_id)


        result = final_result_bi_lstm(session_id)#this gets the final result, define a good fn name

        mongo.db.sessions.insert_one({'session_id': session_id})
        
        return jsonify({'ok': True, 'data': result}), 200

@app.route('/result_text_tranformers', methods = ['GET', 'POST'])
@jwt_required
def result_text_tranformers():
   if request.method == 'POST':
     if request.files:
        uploaded_files_jd = request.files.getlist("jd")
        uploaded_files_cv = request.files.getlist("cv")
        session_id = request.values.get('session_id')
        user = get_jwt_identity()

        mongo_session  = mongo.db.sessions.find_one({"session_id": session_id})


        if mongo_session is None:
          os.makedirs(app.config['UPLOADED_FILES'] + "/" + user["email"]+ "/" + session_id + "/" + "jd")#create folder
          os.makedirs(app.config['UPLOADED_FILES'] + "/" + user["email"]+ "/" + session_id + "/" + "cv")#create folder

          for file in uploaded_files_jd:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOADED_FILES'], user["email"], session_id, "jd" ,filename))
          
          for file in uploaded_files_cv:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOADED_FILES'], user["email"], session_id, "cv" ,filename))
          
          #TEXT EXTRACTION AND CORPUS CREATION
          jd_extraction(session_id)
          cv_extraction(session_id)


        result = final_result_text_transformers(session_id)#this gets the final result, define a good fn name
        mongo.db.sessions.insert_one({'session_id': session_id})
        
        return jsonify({'ok': True, 'data': result}), 200