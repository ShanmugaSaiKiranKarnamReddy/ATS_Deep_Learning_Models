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
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from app import app, mongo, flask_bcrypt, jwt



def main():  # used to make this module imporatble. This is called when the module is imported(a dummy function that does nothing)
    pass


def final_result_keyword_matching(session_id):

    # cluster = MongoClient(
    #     "mongodb+srv://vicky:root123@cluster0.gnmhi.mongodb.net/test")
    # db = cluster["ATS"]

    # local_cluster = MongoClient("localhost:27017")
    # collection_jd_unstruct = db["jd_unstruct"].find()
    # collection_cv_unstruct = db["cv_unstruct"].find()





    JD = ""
    CV = []

    for x in mongo.db.jd_struct.find({"session_id": session_id}):

        JD = x["all_text"]

        

    # resource_manager = PDFResourceManager()

    Key_list = []

    Key1= ['mongodb', 'neo4j', 'redis', 'nosql','Non-Relational Databases', 'db', 'Couchbase', 'Amazon DynamoDB', 'Cassandra', 'Scylla', 'HBase', 'Datastax Enterprise Graph', 'Elasticsearch', 'Splunk', 'Solr']
    flag =0
    for i in range(len(Key1)):
        if Key1[i].lower() in (JD.lower()) != -1 and flag==0:
            Key_list.append(Key1)
            flag = 1


    Key2= ['Oracle','MySQL','Microsoft SQL Server','PostgreSQL','DB2', 'RDBMS', 'Relational Database', 'sql']
    flag =0
    for i in range(len(Key2)):
        if Key2[i].lower() in (JD.lower()) != -1 and flag==0:
            Key_list.append(Key2)
            flag = 1

    Key3= ['HTML','Twitter Bootstrap', 'Skeleton', 'HTML5 Boilerplate', 'HTML KickStart', 'Montage HTML5 Framework', 'Zebra', 'CreateLess Framework', 'SproutCore']
    flag =0
    for i in range(len(Key3)):
        if Key3[i].lower() in (JD.lower()) != -1 and flag==0:
            Key_list.append(Key3)
            flag = 1

    Key4= ['CSS', 'Bootstrap', 'Foundation', 'Bulma', 'UIkit', 'Semantic UI', 'Susy', 'Materialize', 'Pure', 'Skeleton', 'Milligram']
    flag =0
    for i in range(len(Key4)):
        if Key4[i].lower() in (JD.lower()) != -1 and flag==0:
            Key_list.append(Key4)
            flag = 1

    Key5= ['Javascript', 'reactjs','angular', 'angularjs', 'jquery']
    flag =0
    for i in range(len(Key5)):
        if Key5[i].lower() in (JD.lower()) != -1 and flag==0:
            Key_list.append(Key5)
            flag = 1

    Key6= ['Python', 'Growler', 'Giotto', 'Flask', 'Falcon', 'Django', 'Dash', 'CubicWeb', 'CherryPy', 'Bottle', 'AIOHTTP']
    flag =0
    for i in range(len(Key6)):
        if Key6[i].lower() in (JD.lower()) != -1 and flag==0:
            Key_list.append(Key6)
            flag = 1

    Key7= ['PHP', 'Laravel','CodeIgniter' , 'FuelPhp', 'Symfony', 'Zend', 'Phalcon', 'CakePhp', 'Yii']
    flag =0
    for i in range(len(Key7)):
        if Key7[i].lower() in (JD.lower()) != -1 and flag==0:
            Key_list.append(Key7)
            flag = 1

    Key8= ['Ruby', 'Ruby on Rails', 'Padrino', 'Sinatra', 'Hanami', 'Cuba', 'Scorched', 'Grape', 'NYNY', 'Goliath', 'Trailblazer']
    flag =0
    for i in range(len(Key8)):
        if Key8[i].lower() in (JD.lower()) != -1 and flag==0:
            Key_list.append(Key8)
            flag = 1

    Key9= ['C#', 'Automapper', 'Autofixture', 'ASP.NET MVC', 'ASP.NET WEBAPI', 'NancyFX', 'Common Logging', 'Windsor Container', 'Service Stack', 'Quartz.NET', 'SignalIR']
    flag =0
    for i in range(len(Key9)):
        if Key9[i].lower() in (JD.lower()) != -1 and flag==0:
            Key_list.append(Key9)
            flag = 1

    Key10= ['Tableau', 'Tableau Public', 'Infogram', 'ChartBlocks', 'Datawrapper', 'D3.js', 'Google Charts', 'FusionCharts', 'Chart.js', 'Grafana', 'Chartist.js', 'Sigmajs', 'Polymaps', 'Adobe Creative Cloud', 'Chart Studio', 'Plotly', 'DataHero', 'RAWGraphs', 'Dygraphs', 'ZingChart', 'InstantAtlas', 'Modest Maps', 'Leaflet', 'WolframAlpha', 'Visualize Free', 'Better World Flux', 'jqPlot', 'JavaScript InfoVis Toolkit', 'jpGraph', 'Highcharts', 'Excel', 'CSV/JSON', 'Crossfilter', 'Tangle', 'OpenLayers', 'Kartograph', 'Carto', 'Processing.js', 'NodeBox', 'Weka', 'Gephi', 'iCharts', 'Flot', 'infographic', 'PowerBI']
    flag =0
    for i in range(len(Key10)):
        if Key10[i].lower() in (JD.lower()) != -1 and flag==0:
            Key_list.append(Key10)
            flag = 1



    mydict = {}
    # if statment to check the file type 
    # a for loop for raw text 
    for file in mongo.db.cv_struct.find({"session_id":session_id}):
        Content = file["all_text"]
        score =0
        for x in Key_list:
            i = 0
            for y in x:
                if y.lower() in (Content.lower()) != -1:
                    i = i+1
                    # print(y)
            # print(i)
            score = i+score
        mydict[file["file_name"]] = score
        # fake_file_handle.close()
        # converter.close()
    # print(mydict)


    return {k: v for k, v in sorted(mydict.items(), key=lambda item: item[1], reverse = True)}


if __name__ == "__main__":
  main()

# resume_scores_dict()
