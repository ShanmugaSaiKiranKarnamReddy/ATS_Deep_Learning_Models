# Inserting JD and Resumes into MongoDb
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.converter import TextConverter
import io
from os import listdir
from os.path import isfile, join
from pymongo import MongoClient
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pymongo import MongoClient
import pandas as pd

from nltk import word_tokenize, sent_tokenize

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer  # register thing
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import cosine_similarity


def main():  # used to make this module imporatble. This is called when the module is imported(a dummy function that does nothing)
    pass


def get_tfidf_result(session_id):

    cluster = MongoClient(
        "mongodb+srv://vicky:root123@cluster0.gnmhi.mongodb.net/test")
    db = cluster["ATS"]

    collection_jd_unstruct = db["jd_unstruct"].find()
    collection_cv_unstruct = db["cv_unstruct"].find()

    ###########
    # WORKING PROPERLY: reads texts from all resume pdfs, any number of pages
    #########

    JD_data = collection_jd_unstruct
    JD_dataFrame = pd.DataFrame(JD_data)

    CV_data = collection_cv_unstruct
    CV_dataFrame = pd.DataFrame(CV_data)

    print(JD_data, CV_data)

    # for x in local_collection_jd_unstruct.find():
    #   JD = x["text"]
    #   print(JD)

    # Retrieving data from MongoDB - JD & Resumes

    #cluster = MongoClient('mongodb://localhost:27017/')
    with cluster:
        db = cluster['ATS']
    Data = db["test"].find({})
    data = pd.DataFrame(Data)

    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()

    def clean_text(text):
        text = text.lower()
        text = text.replace("\n", " ")
        text = re.sub(r'\W+', ' ', text)
        text_tokens = word_tokenize(text)
        text = [lemmatizer.lemmatize(token, pos="v") for token in text_tokens]
        tokens = [word for word in text if not word in stopwords.words()]
        text = " ".join(tokens)
        return [tokens, text]

    # Base Model

    def TfIdf(text):
        # Tf-Idf
        tfidf_vectorizer = TfidfVectorizer()
        TfIdf_features = tfidf_vectorizer.fit_transform(text)
        return TfIdf_features

    # Python code to pre-process text
    #print(JD_dataFrame, "here")

    mydict = {}

    t_jd = JD_dataFrame["text"].apply(clean_text)
    JD_dataFrame['tokens'] = [item[0] for item in t_jd]  # Tokenization
    JD_dataFrame['pp_text'] = [item[1] for item in t_jd]  # Cleaned text

    t_cv = CV_dataFrame["text"].apply(clean_text)
    CV_dataFrame['tokens'] = [item[0] for item in t_cv]  # Tokenization
    CV_dataFrame['pp_text'] = [item[1] for item in t_cv]  # Cleaned text

    for i in range(len(CV_dataFrame)-1):
        a = TfIdf([CV_dataFrame.pp_text[i], JD_dataFrame.pp_text[0]])
        val = cosine_similarity(a, a)
        print("Resume: {}     %Similarity: {}".format(
            CV_dataFrame["file_name"][i], val[1][0]*100))
        mydict[CV_dataFrame["file_name"][i]] = val[1][0]*100

    print({k: v for k, v in sorted(mydict.items(), key=lambda item: item[1], reverse=True)})
    return {k: v for k, v in sorted(mydict.items(), key=lambda item: item[1], reverse=True)}


if __name__ == "__main__":
    main()
