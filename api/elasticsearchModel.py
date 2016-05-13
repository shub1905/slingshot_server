from collections import defaultdict
import elasticsearch
import json


class ElasticSearch:

    def __init__(self):
        config_file = open('config.json', 'r')
        config = json.loads(config_file.read())['elasticsearch']
        self.index = config['index']
        self.index_group = config['index_group']
        self.doc = config['doc']
        self.conn = elasticsearch.Elasticsearch(config['host'])

    def save_metadata(self, json_data):
        print self.conn.index(self.index, self.doc, json_data)

    def update_metadata(self, json_data):
        pass

    def fetch_metadata(self, uuid):
        query = {
            "query": {
                "match_phrase": {
                    "uuid": uuid
                }
            }
        }
        response = self.conn.search(self.index_group, self.doc, body=query)
        img_groups = defaultdict(list)

        for res in response['hits']['hits']:
            img = res['_source']
            img_groups[img['name']] += img['groups_id']

        return img_groups

    def fetch_metadata_group(self, uuid, tag):
        query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "term": {
                                "uuid": {
                                    "value": uuid
                                }
                            }
                        },
                        {
                            "term": {
                                "groups_id": {
                                    "value": tag
                                }
                            }
                        }
                    ]
                }
            }
        }
        response = self.conn.search(self.index_group, self.doc, body=query)
        img_list = []

        for res in response['hits']['hits']:
            img = res['_source']
            img_list.append('../../images/{}/{}'.format(uuid, img['name']))

        return img_list

    def fetch_all_images(self, uuid):
        query = {
            "query": {
                "match_phrase": {
                    "uuid": uuid
                }
            }
        }
        response = self.conn.search(self.index, self.doc, body=query)
        return response

    def save_group_info(self, groups, uuid):
        body = {
            "uuid": str(uuid)
        }
        for gp in groups:
            body['name'] = str(gp)
            body['groups_id'] = map(int, groups[gp])
            print self.conn.index(self.index_group, self.doc, body, id=body['name'])

elastic = ElasticSearch()
