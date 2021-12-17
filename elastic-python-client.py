#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# import the run and get methods from the bottle library
from bottle import run, get

# import the elasticsearch client library
from elasticsearch import Elasticsearch

# import Python's json library to format JSON responses
import json

# use codecs to open the existing HTML file
import codecs

# globals for the Elasticsearch domain
# ResourceWarning: unclosed <socket.socket> error if HTTP in domain
DOMAIN = "localhost"
ELASTIC_PORT = 9200
BOTTLE_PORT = 1234

try:

    # concatenate a string for the Elasticsearch connection
    domain_str = DOMAIN + ":" + str(ELASTIC_PORT)

    # declare a client instance of the Python Elasticsearch library
    client = Elasticsearch( domain_str )

    # info() method raises error if domain or conn is invalid
    print (json.dumps( Elasticsearch.info(client), indent=4 ), "\n")

except Exception as err:
    print ("Elasticsearch() ERROR:", err, "\n")

    # client is set to none if connection is invalid
    client = None

def get_elasticsearch_data(client, query={}, page=0):
    # create a dict for the Elasticsearch docs
    all_docs = {}

    # make API call if client is not None
    if client != None:

        # returns a list of all the cluster's indices
        all_indices = client.indices.get_alias("*")

        # iterate over the index names
        for ind in all_indices:

            # skip hidden indices with '.' in name
            if "." not in ind[:1]:

                # nest another dictionary for index inside
                all_docs[ ind ] = {}

                # print the index name
                print ( "\nindex:", ind )

                # get 10 of the Elasticsearch documents from index
                docs = client.search(
                    from_ = page, # for pagination
                    index = ind,
                    body = {
                        'size' : 10,
                        'query': {
                            # pass query paramater
                            'match_all' : query
                        }
                })

                # get just the doc "hits"
                docs = docs["hits"]["hits"]

                # print the list of docs
                print ("index:", ind, "has", len(docs), "num of docs.")

                # put the list of docs into a dict key
                all_docs[ ind ]["docs"] = docs

                try:
                    # returns dict object of the index _mapping schema
                    raw_data = client.indices.get_mapping( ind )
                    print ("get_mapping() response type:", type(raw_data))

                    # returns dict_keys() obj in Python 3
                    mapping_keys = raw_data[ ind ]["mappings"].keys()
                    print ("\n_mapping keys():", mapping_keys)

                    # get the index's doc type
                    doc_type = list(mapping_keys)[0]
                    print ("doc_type:", doc_type)

                    # get the schema by accessing index's _doc type
                    schema = raw_data[ ind ]["mappings"][ doc_type ]["properties"]
                    print ("all fields:", list(schema.keys()) )

                    all_docs[ ind ]["fields"] = schema
                    all_docs[ ind ]["doc_type"] = doc_type
                except Exception as err:
                    print ("client.indices error:", err)
                    all_docs[ ind ]["fields"] = {}
                    all_docs[ ind ]["doc_type"] = doc_type

    # return all of the doc dict
    return all_docs

# get a function that will return HTML string for frontend
def html_elasticsearch():

    html_file = codecs.open("index.html", 'r')
    html = html_file.read()

    # get all of the Elasticsearch indices, field names, & documents
    elastic_data = get_elasticsearch_data(client)

    # if there's no client then show on frontend
    if client != None:

        print ("html_elasticsearch() client:", client)

        # iterate over the index names
        for index, val in elastic_data.items():

            # create a new HTML table from the index name
            html += '<br><h3>Index name: ' + str(index) + '</h3>'
            html += '<table id="' + str(index) + '" class="table table-responsive">'

            # grab the "fields" list attribute created in get_elasticsearch_data()
            fields = source_data = elastic_data[index]["fields"]
            print ("\n\nfields:", fields)

            # new table row
            html += '\n<tr>'

            # enumerate() over the index fields
            for num, field in enumerate(fields):
                html += '<th>' + str(field) + '</th>'

            # close the table row for the Elasticsearch index fields
            html += '\n</tr>'

            # get all of the docs in the Elasticsearch index
            all_docs = elastic_data[index]["docs"]
            print ("\nall_docs type:", type(all_docs))

            # enumerate() over the list of docs
            for num, doc in enumerate(all_docs):
                print ("\ndoc:", doc)

                # new row for each doc
                html += '<tr>\n'

                # iterate over the _source dict for the doc
                for f, val in doc["_source"].items():
                    html += '<td>' + str(val) + '</td>'
               
                html += '</tr>'

            # close the table tag for the Elasticsearch index
            html += '</table><br>'
    elif client == None:
        html += '<h3 style="color:red">Warning: Elasticsearch cluster is not running on'
        html += ' port: ' + str(ELASTIC_PORT) + '</h3>'
    elif elastic_data == {}:
        html += '<h3>Elasticsearch did not return index information</h3>'

    # return the HTML string
    return html + "</body></html>\n\n"

@get('/')
def elastic_app():
    # call the func to return HTML to framework
    return html_elasticsearch()

# pass a port for the framework's server
run(
    host = DOMAIN,
    port = BOTTLE_PORT,
    debug = True
)