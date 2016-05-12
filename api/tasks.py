from __future__ import absolute_import

from celery import shared_task
from api.elasticsearchModel import elastic
from alchemyapi import AlchemyAPI
import os
import json
from PIL import Image
al = AlchemyAPI()


@shared_task
def process_image(uuid, path):
  print path
  manage_image_size(path)
  response = al.faceTagging('image', path)
  if response['status'] == 'OK':
    response['uuid'] = uuid
    del(response['usage'])
    elastic.save_metadata(response)
    crop_faces.apply_async((response, path))


@shared_task
def manage_image_size(path):
  size = os.path.getsize(path)
  if size > 10**6:
    return False


@shared_task
def crop_faces(response, path):
  im = Image.open(path)
  faces = []
  for img_attr in response['imageFaces']:
    att = [img_attr['positionX'], img_attr['positionY'], img_attr['height'],  img_attr['width']]
    att = map(float, att)
    box = (att[0], att[1], att[0]+att[2], att[1]+att[3])
    region = im.crop(box)
    faces.append(region)

  for i, f in enumerate(faces):
    pth = '{}_{}.jpg'.format(path, i)
    print pth
    f.save(pth, "JPEG")
