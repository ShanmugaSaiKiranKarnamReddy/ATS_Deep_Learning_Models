from flask import Flask, render_template, request
# from Settings. security import authenticate, identity
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
from pathlib import Path

import importlib.util
from ocr.TesseractMain import get_raw_text
from tfidf.tfidf_main import get_tfidf_result
from keywordmatching.KeyWordMatching import keyword_matching

import time
from textextraction.cv_extraction import CVExtraction
from textextraction.jd_extraction import JDExtraction
#from punctuator2 import punctuator
#test = subprocess.Popen(["cat", "test.txt" "|" "python3" "punctuator.py" "./models/Punctuator2/Demo-Europarl-EN.pcl" "output.txt"], stdout=subprocess.PIPE)




app = Flask(__name__)
CORS(app, supports_credentials=True)#CORS fixes server side
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] =  "123445"

dir = os.path.dirname(__file__)


import datetime

app.config['MONGODB_SETTINGS'] = {
    'db': 'ATS',
    'host': 'mongodb+srv://vicky:root123@cluster0.gnmhi.mongodb.net/test'
}

app.config['SECRET_KEY'] = '9776973925'


@app.route('/', methods = ['GET', 'POST'])
def home():
  print("refreshed")
  return "okay"


#one script to convert pdf or image to raw text and store in mongo #Important
@app.route('/uploadJD', methods = ['GET', 'POST'])
def upload_file_jd():
   if request.method == 'POST':
     if request.files:
        uploaded_files = request.files.getlist("file")
        session_id = request.headers.get('Session-Id')
        os.makedirs('./files/uploads/' + session_id + '/jdfile')
        app.config['UPLOAD_FOLDER_JD'] = os.path.join(dir, './files/uploads/' + session_id + '/jdfile')
        for file in uploaded_files:
          file.save(os.path.join(app.config['UPLOAD_FOLDER_JD'], file.filename))
        
        JDExtraction(session_id)
        #test.communicate()[0]
        return "JD succesfully uploaded"
        

      

@app.route('/uploadCV', methods = ['GET', 'POST'])
def upload_file_cv():
   if request.method == 'POST':
      if request.files:
        uploaded_files = request.files.getlist("file")
        session_id = request.headers.get('Session-Id')
        os.makedirs('./files/uploads/' + session_id + '/cvfiles')
        app.config['UPLOAD_FOLDER_CV'] = os.path.join(dir, './files/uploads/' + session_id + '/cvfiles')

        for file in uploaded_files:
          file.save(os.path.join(app.config['UPLOAD_FOLDER_CV'], file.filename))
        
        CVExtraction(session_id)
        # return "CV successfully uploaded"
        return {"dict_result": keyword_matching(session_id), "tfidf_result": get_tfidf_result(session_id)}

# @app.route('/getTFIDFResult', methods = ['GET', 'POST'])
# def getTFIDFResult():
#    if request.method == 'GET':
#       return get_tfidf_result()

@app.route('/get_time', methods = ['GET', 'POST'])
def	get_time():
  if request.method == 'GET':
    return 'GET request test'

#routes end

if __name__ == '__main__':
   app.run(debug=True, port=3001)

