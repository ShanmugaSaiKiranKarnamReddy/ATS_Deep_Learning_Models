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

from tfidf.tfidf_main import get_tfidf_result
from keywordmatching.KeyWordMatching import keyword_matching

import glob
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.converter import TextConverter
import io



def main():#used to make this module imporatble. This is called when the module is imported(a dummy function that does nothing)
  pass


def CVExtraction(session_id):
  cluster = MongoClient("mongodb+srv://vicky:root123@cluster0.gnmhi.mongodb.net/test")
  db = cluster["ATS"]

  collection_cv_struct = db["cv_struct"]
  collection_cv_unstruct = db["cv_unstruct"]

  dir = os.path.dirname(__file__)




  rootdirCV = os.path.join(dir, '../files/uploads/' + session_id +'/cvfiles/')




  for filename in os.listdir(rootdirCV):

    if filename.endswith(".jpeg") or filename.endswith(".jpg"):
      img = Image.open(rootdirCV + filename)#silly bug
      text = tess.image_to_string(img)
      text_lower = text.lower()
      tx = " ".join(text_lower.split('\n'))#split at space?
      print(tx)
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
        
        collection_cv_unstruct.insert_one({"file_name": filename, "text": Content})
        #for structured data for training data model
        pdf_data = ResumeParser(rootdirCV + filename).get_extracted_data()
        pdf_data["file_name"] = filename
        #os.system('cat' + Content + ' | python ../punctuator2/models/Punctuator2/Demo-Europarl-EN.pcl  output.txt ')
        pdf_data["all_text"] = Content
        pdf_data["session_id"] = session_id

        print(filename)
        collection_cv_struct.insert_one(pdf_data)
        # return keyword_matching()


if __name__ == "__main__":
  main()


# CVExtraction()