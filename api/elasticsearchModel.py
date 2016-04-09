import elasticsearch
import json


class ElasticSearch:

    def create_connection(self):
        config_file = open('config.json', 'r')
        config = json.loads(config_file.read())['elasticsearch']
        self.connection = elasticsearch.Elasticsearch(host=config['host'], port=config['port'])
        return self.connection

    def save_metadata(self, json_data):
        pass

    def update_metadata(self, json_data):
        pass

    def fetch_metadata(self, image_id):
        pass

elastic = Elasticsearch()