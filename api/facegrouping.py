from elasticsearchModel import elastic
from collections import defaultdict
from clustering import cluster
from PCA import pca_model
from PIL import Image
import numpy
import os


def extract_X(uuid):
    response = elastic.fetch_all_images(uuid)
    img_names = []
    for res in response['hits']['hits']:
        for file_name in res['_source']['files']:
            img_names.append((file_name, res['_source']['name']))

    X = numpy.zeros((len(img_names), 100 * 100 * 3))
    for i, face_img_path in enumerate(img_names):
        im = Image.open(face_img_path[0])
        im = numpy.array(im).flatten()
        X[i, :] = im

    X_red = pca_model.dim_reduction(X)
    return X_red, img_names


def group_pics(uuid):
    X, names = extract_X(uuid)
    groups = cluster.cluster(X, names)
    img_gps = defaultdict(list)
    for gp in groups:
        for img in groups[gp]:
            img_gps[img].append(gp)
    return img_gps
