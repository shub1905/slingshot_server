from __future__ import absolute_import
from api.elasticsearchModel import elastic
from api.facegrouping import group_pics
from alchemyapi import AlchemyAPI
from celery import shared_task
from PIL import Image
import json
import os

al = AlchemyAPI()


@shared_task
def process_image(uuid, path, filename):
    manage_image_size(path)
    response = al.faceTagging('image', path)
    if response['status'] == 'OK':
        response['uuid'] = uuid
        response['name'] = filename
        del(response['usage'])
        del(response['NOTICE'])
        response['files'] = crop_faces(response, path)
        elastic.save_metadata(response)


def manage_image_size(path):
    size = os.path.getsize(path)
    rez = 500
    if size > 10**6:
        im = Image.open(path)
        print im.size
        size = (rez, int(im.size[1]*1.*rez/im.size[0]))
        im = im.resize(size, Image.ANTIALIAS)
        print im.size
        im.save(path, "JPEG")


def crop_faces(response, path):
    im = Image.open(path)
    faces = []
    for img_attr in response['imageFaces']:
        att = [img_attr['positionX'], img_attr['positionY'], img_attr['height'],  img_attr['width']]
        att = map(int, att)
        box = (att[0], att[1], att[0] + att[2], att[1] + att[3])
        region = im.crop(box).resize((100, 100), Image.ANTIALIAS)
        faces.append(region)

    file_names = []
    for i, f in enumerate(faces):
        pth = '{}_{}_crop.jpg'.format(path[:-4], i)
        # file_names.append({'path':pth, 'group': 'NA'})
        file_names.append(pth)
        f.save(pth, "JPEG")
    return file_names


@shared_task
def cluster_pics(uuid):
    groups = group_pics(uuid)
    elastic.save_group_info(groups, uuid)
