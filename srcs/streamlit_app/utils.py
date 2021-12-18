# srcs/streamlit_app/utils.py
from elasticsearch import Elasticsearch
from datetime import date

DOMAIN = 'es'
es = Elasticsearch(host=DOMAIN)

def index_search(education_level, sector_selected):
    results = es.search(index="qp-name", 
                    query = {"bool": {"must": [
                    {"match": {"Educational Qualification" : education_level}},
                    {"match": {"Sector" : sector_selected }},
                    ]
                }})
    return results

# Python3 code to calculate age in years
def calculateAge(birthDate):
    days_in_year = 365.2425
    age = int((date.today() - birthDate).days / days_in_year)
    return age
