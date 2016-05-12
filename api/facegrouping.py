from elasticsearchModel import elastic
from PIL import Image
import numpy
import os

def regroup_faces(uuid):
    response = elastic.fetch_all_images(uuid)
    img_names = []
    for res in response['hits']['hits']:
        for file_name in res['_source']['files']:
            img_names.append(file_name)

    X = numpy.zeros((len(img_names), 100*100*3))
    for i,face_img_path in enumerate(img_names):
        im = Image.open(face_img_path)
        im = numpy.array(im).flatten()
        X[i,:] = im

    print X.shape
