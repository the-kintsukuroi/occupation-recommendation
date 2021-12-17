# srcs/streamlit_app/utils.py
from elasticsearch import Elasticsearch
es = Elasticsearch()

def index_search(education_level, sector_selected):
    result = es.search(index="qp-name", 
                    query = {"bool": {"must": [
                    {"match": {"Educational Qualification" : education_level}},
                    {"match": {"Sector" : sector_selected }},
                    ]
                }})
    print("Got %d Hits:" % result['hits']['total']['value'])
 