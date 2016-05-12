import elasticsearch
import json


class ElasticSearch:

    def __init__(self):
        config_file = open('config.json', 'r')
        config = json.loads(config_file.read())['elasticsearch']
        self.index = config['index']
        self.doc = config['doc']
        self.conn = elasticsearch.Elasticsearch(
            host=config['host'], port=config['port'])

    def save_metadata(self, json_data):
        print self.conn.index(self.index, self.doc, json_data)

    def update_metadata(self, json_data):
        pass

    def fetch_metadata(self, image_ids):
        meta = []
        for img_id in image_ids:
            print img_id
            meta.append(self.conn.get(self.index, self.doc, img_id))
        return meta

    def fetch_all_images(self, uuid):
        query = {
            "query": {
                "match_phrase": {
                    "uuid": uuid
                }
            }
        }
        response = self.conn.search(self.index, body=query)
        return response

elastic = ElasticSearch()
