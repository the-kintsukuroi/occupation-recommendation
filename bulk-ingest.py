#!/usr/bin/env python
# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

# Reference - https://github.com/elastic/elasticsearch-py/blob/main/examples/bulk-ingest/bulk-ingest.py

# Terminal command
# cd /Users/karshi/elasticsearch-7.15.2
# ./bin/elasticsearch

"""Script that streams data to an Elasticsearch cluster"""

import csv
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

DATASET_PATH = 'import-data.csv'

def create_index(client):
    """Creates an index in Elasticsearch if one isn't already there."""
    client.indices.create(
        index="qp-name",
        body={
            "settings": {"number_of_shards": 1}
            },
        ignore=400,
    )


def generate_actions():
    """Reads the file through csv.DictReader() and for each row
    yields a single document. This function is passed into the bulk()
    helper to create many documents in sequence.
    """
    with open(DATASET_PATH, mode="r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            doc = json.dumps(row)
            yield doc


def main():
    client = Elasticsearch(
        # Add your cluster configuration here!
    )
    print("Creating an index...")
    create_index(client)
    print("Indexing documents...")
    for action in streaming_bulk(client=client, index="qp-name", actions=generate_actions()):
        print("Indexed a document")

if __name__ == "__main__":
    main()