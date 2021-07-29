import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import Image
import json
import pymongo
import json
from json import loads
from pymongo import MongoClient
import os
from os.path import isfile, join

import glob
# from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.converter import TextConverter
import io


def get_raw_text(file_type):#responsoble for storing file (pdf, image) in fs and extract text and store it in mongo
  cluster = MongoClient("mongodb+srv://vicky:vicky@casestudy1.x7cc1.mongodb.net/<dbname>?retryWrites=true&w=majority")
  db = cluster["ATS"]
  # collection = db["test"]

  local_cluster = MongoClient("localhost:27017")
  local_db = local_cluster["ATS"]
  # local_collection_test = local_db["test"]
  # local_collection_imagedata = local_db["imagedata"]
  local_collection_cv_struct = local_db["cv_struct"]
  local_collection_jd_struct = local_db["jd_struct"]
  local_collection_jd_unstruct = local_db["jd_unstruct"]
  local_collection_cv_unstruct = local_db["cv_unstruct"]

  rootdirJD = 'C://Users//Vicky//source//universityWork//case-study-1-october2019-case-study-group-2//app//backend//files//uploads//jdfiles//'
  rootdirCV = 'C://Users//Vicky//source//universityWork//case-study-1-october2019-case-study-group-2//app//backend//files//uploads//cvfiles//'
  testdir= 'C://Users//Vicky//source//universityWork//case-study-1-october2019-case-study-group-2//app//backend//files//uploads//allfiles//'



  active_local_collection_unstruct =  None
  active_local_collection_struct =  None
  active_root_directory = None

  if file_type == "update_jd":
    active_local_collection_unstruct = local_collection_jd_unstruct
    active_local_collection_struct = local_collection_jd_struct
    active_root_directory = rootdirJD
  elif file_type == "update_cv":
    active_local_collection_unstruct = local_collection_cv_unstruct
    active_local_collection_struct = local_collection_cv_struct
    active_root_directory = rootdirCV
  
  

  for filename in enumerate(os.listdir(active_root_directory)):


    if filename.endswith(".jpeg") or filename.endswith(".jpg"):
      img = Image.open(active_root_directory + filename)#silly bug
      text = tess.image_to_string(img)
      text_lower = text.lower()
      tx = " ".join(text_lower.split('\n'))#split at space? 
      #local_collection_cv.insert_one({"file_name": filename, "text": tx})
    elif filename.endswith(".pdf") or filename.endswith(".docx"):
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        doc = join(active_root_directory, filename)
        fhandle = open(doc, 'rb')

        for page in PDFPage.get_pages(fhandle, caching=False, check_extractable=True):
            page_interpreter.process_page(page)
        
        
        Content = fake_file_handle.getvalue()
        score =0
        Content = fake_file_handle.getvalue()
        
        active_local_collection_unstruct.insert_one({"file_name": filename, "text": Content})
        #for structured data for training data model
        pdf_data = ResumeParser(active_root_directory + filename).get_extracted_data()
        pdf_data["file_name"] = filename
        active_local_collection_struct.insert_one(pdf_data)
 


if __name__ == "__main__":#use this only when this module is exported
   get_raw_text()
