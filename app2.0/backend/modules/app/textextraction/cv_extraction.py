import pytesseract as tess
#tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import Image
import json
import pymongo
import json
from json import loads
from pymongo import MongoClient
import os
from os.path import isfile, join
from app import app, mongo, flask_bcrypt, jwt
# from tfidf.tfidf_main import get_tfidf_result
# from keywordmatching.KeyWordMatching import keyword_matching
from ..corpusextraction import extract_cv_corpus

import glob
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.converter import TextConverter
import io
from app import app, mongo, flask_bcrypt, jwt
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)


def main():#used to make this module imporatble. This is called when the module is imported(a dummy function that does nothing)
  pass


def cv_extraction(session_id):
  user = get_jwt_identity()


  from pathlib import Path
  rootdirCV = Path( app.config['UPLOADED_FILES'], user["email"], session_id, "cv")




  #rootdirCV = os.path.join(dir, '../files/uploads/' + session_id +'/cvfiles/')




  for filename in os.listdir(rootdirCV):

    if filename.endswith(".jpeg") or filename.endswith(".jpg"):
      img = Image.open(rootdirCV + filename)
      text = tess.image_to_string(img)
      text_lower = text.lower()
      tx = " ".join(text_lower.split('\n'))#split at space?
      # print(tx)
      #local_collection_cv.insert_one({"file_name": filename, "text": tx})
    elif filename.endswith(".pdf") or filename.endswith(".docx"):
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        doc = join(rootdirCV, filename)
        fhandle = open(doc, 'rb')

        for page in PDFPage.get_pages(fhandle, caching=False, check_extractable=True):
            page_interpreter.process_page(page)
        
        
        Content = fake_file_handle.getvalue()
        Content = fake_file_handle.getvalue()
        
        #for structured data for training data model
        pdf_data = ResumeParser(str(rootdirCV) + "/" + str(filename)).get_extracted_data()
        pdf_data["file_name"] = filename
        pdf_data["all_text"] = Content
        pdf_data["session_id"] = session_id
        pdf_data["user_id"] = user["email"]
        pdf_data["doc_type"] = "cv"
        cur = mongo.db.users.find({"email": user["email"]})

        for doc in cur:
          # print(doc['_id'])
          pdf_data["user_mongo_object_id"] = doc['_id']


        mongo.db.cv_struct.insert_one(pdf_data)
        extract_cv_corpus(session_id)


if __name__ == "__main__":
  main()


# CVExtraction()