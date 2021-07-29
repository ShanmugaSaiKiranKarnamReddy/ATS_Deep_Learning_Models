''' controller and routes for upload '''
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
# from textextraction.cv_extraction import CVExtraction
from ..textextraction import jd_extraction
from ..textextraction import cv_extraction
import uuid

# ROOT_PATH = os.environ.get('ROOT_PATH')
# LOG = logger.get_root_logger(
#     __name__, filename=os.path.join(ROOT_PATH, 'output.log'))

@app.route('/upload', methods = ['GET', 'POST'])
@jwt_required
def home():
  print("refreshed")
  user = get_jwt_identity()
  return jsonify({'ok': True, 'data': user}), 200


@app.route('/start', methods = ['GET', 'POST'])
@jwt_required
def start():
  session_id = str(uuid.uuid4()) #created uuid to track a session
  return jsonify({'ok': True, 'session_id': session_id}), 200

@app.route('/uploadJD', methods = ['GET', 'POST'])
@jwt_required
def upload_file_jd():
   if request.method == 'POST':
     if request.files:
        uploaded_files = request.files.getlist("file")
        session_id = request.values.get('session_id')
        user = get_jwt_identity()
        os.makedirs(app.config['UPLOADED_FILES'] + "/" + user["email"]+ "/" + session_id + "/" + "jd")#create folder
        for file in uploaded_files:
          filename = secure_filename(file.filename)
          file.save(os.path.join(app.config['UPLOADED_FILES'], user["email"], session_id, "jd" ,filename))
        
        jd_extraction(session_id)
        #test.communicate()[0]
        return jsonify({'ok': True, 'uploaded': True}), 200


@app.route('/uploadCV', methods = ['GET', 'POST'])
@jwt_required
def upload_file_cv():
   if request.method == 'POST':
     if request.files:
        uploaded_files = request.files.getlist("file")
        session_id = request.values.get('session_id')
        user = get_jwt_identity()

        if not os.path.exists(app.config['UPLOADED_FILES'] + "/" + user["email"]+ "/" + session_id + "/" + "cv"):
          os.makedirs(app.config['UPLOADED_FILES'] + "/" + user["email"]+ "/" + session_id + "/" + "cv")#create folder
        for file in uploaded_files:
          filename = secure_filename(file.filename)
          file.save(os.path.join(app.config['UPLOADED_FILES'], user["email"], session_id, "cv" ,filename))
        
        cv_extraction(session_id)
        #test.communicate()[0]
        return jsonify({'ok': True, 'uploaded': True}), 200