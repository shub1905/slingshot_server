from __future__ import absolute_import

from celery import shared_task
from api.elasticsearchModel import elastic
from alchemyapi import AlchemyAPI
import os
import json
from PIL import Image
from api.facegrouping import group_pics
al = AlchemyAPI()


@shared_task
def process_image(uuid, path, filename):
    print path
    manage_image_size(path)
    response = al.faceTagging('image', path)
    if response['status'] == 'OK':
        response['uuid'] = uuid
        response['name'] = filename
        del(response['usage'])
        response['files'] = crop_faces(response, path)
        elastic.save_metadata(response)


def manage_image_size(path):
    size = os.path.getsize(path)
    if size > 10**6:
        return False


def crop_faces(response, path):
    im = Image.open(path)
    faces = []
    for img_attr in response['imageFaces']:
        att = [img_attr['positionX'], img_attr['positionY'], img_attr['height'],  img_attr['width']]
        att = map(float, att)
        box = (att[0], att[1], att[0] + att[2], att[1] + att[3])
        region = im.crop(box).resize((100, 100))
        faces.append(region)

    file_names = []
    for i, f in enumerate(faces):
        pth = '{}_{}.jpg'.format(path[:-4], i)
        # file_names.append({'path':pth, 'group': 'NA'})
        file_names.append(pth)
        f.save(pth, "JPEG")
    return file_names


@shared_task
def cluster_pics(uuid):
    groups = group_pics(uuid)
    elastic.save_group_info(groups, uuid)
