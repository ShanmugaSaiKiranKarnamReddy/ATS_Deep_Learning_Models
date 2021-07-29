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
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from ..corpusextraction import extract_jd_corpus


import glob
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.converter import TextConverter
import io
from ..corpusextraction import extract_jd_corpus
# from punctuator2 import punctuator


def main():
  pass

def jd_extraction(session_id):
  user = get_jwt_identity()


  from pathlib import Path
  rootdirJD = Path( app.config['UPLOADED_FILES'], user["email"], session_id, "jd")


  for filename in os.listdir(rootdirJD):
    # print(filename)
    if filename.endswith(".png"):
      img = Image.open(str(rootdirJD) + "/" + str(filename))
      text = tess.image_to_string(img)
      # print(text, "lolwa")
      pdf_data = ResumeParser(str(rootdirJD) + "/" + str(filename)).get_extracted_data()
      print(pdf_data, "lolwa")

    elif filename.endswith(".pdf") or filename.endswith(".docx"):
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        doc = join(rootdirJD, filename)
        fhandle = open(doc, 'rb')

        for page in PDFPage.get_pages(fhandle, caching=False, check_extractable=True):
            page_interpreter.process_page(page)
        
        
        Content = fake_file_handle.getvalue()
        
      
        #for structured data for training data model
        #find a better Parser for JD
        pdf_data = ResumeParser(str(rootdirJD) + "/" + str(filename)).get_extracted_data()
        pdf_data["file_name"] = filename
        pdf_data["all_text"] = Content
        pdf_data["session_id"] = session_id
        pdf_data["user_id"] = user["email"]
        pdf_data["doc_type"] = "jd"
        cur = mongo.db.users.find({"email": user["email"]})

        for doc in cur:
          # print(doc['_id'])
          pdf_data["user_mongo_object_id"] = doc['_id']
        #create corpus as well


        mongo.db.jd_struct.insert_one(pdf_data)
        extract_jd_corpus(session_id)

if __name__ == "__main__":
  main()
