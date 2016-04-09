import elasticsearch
import json


class ElasticSearch:

    def __init__(self):
        config_file = open('config.json', 'r')
        config = json.loads(config_file.read())['elasticsearch']
        self.index = config['index']
        self.doc = config['doc']
        self.conn = elasticsearch.Elasticsearch(host=config['host'], port=config['port'])

    def save_metadata(self, json_data):
        print self.conn.index(self.index, self.doc, json_data)

    def update_metadata(self, json_data):
        pass

    def fetch_metadata(self, image_id):
        pass

elastic = ElasticSearch()