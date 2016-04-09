from __future__ import absolute_import

from celery import shared_task
from api.elasticsearchModel import elastic
from alchemyapi import AlchemyAPI

al = AlchemyAPI()

@shared_task
def process_image(uuid, path):
	response = al.faceTagging('image', path)
	if response['status'] == 'OK':
		elastic.save_metadata(response)