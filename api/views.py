from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from api.elasticsearchModel import elastic
import tasks
import uuid
import json
import os
import pdb
from uploader.models import UploadForm, Upload


def userid(request):
    response_data = {}
    response_data['uuid'] = uuid.uuid1()
    response_data['message'] = 'This is the unique user id'
    return JsonResponse(response_data)


def upload(request):
    if request.method == 'POST':
        save_file(request.FILES['image'], request.POST.get('uuid', 'unnamed'))
        return HttpResponse('Thanks for uploading the image')
    return HttpResponse('Something bad happened')


def save_file(file, uuid):
    ''' Little helper to save a file'''
    MEDIA_ROOT = os.getcwd() + '/images/' + uuid
    if not os.path.exists(MEDIA_ROOT):
        os.makedirs(MEDIA_ROOT)
    filename = file._get_name()

    file_path = '%s/%s' % (MEDIA_ROOT, str(filename))
    fd = open(file_path, 'wb')
    for chunk in file.chunks():
        fd.write(chunk)
    fd.close()
    tasks.process_image.apply_async((uuid, file_path, filename))


def list_images(request):
    uuid = request.GET.get('uuid', 'test')
    MEDIA_ROOT = os.getcwd() + '/images/{}'.format(uuid)
    if not os.path.exists(MEDIA_ROOT):
        os.makedirs(MEDIA_ROOT)
    images = []

    for img in os.listdir(MEDIA_ROOT):
        if img.endswith('crop.jpg'):
            continue
        temp = '../../images/{}/{}'.format(uuid, img)
        images.append(temp)

    context = {"images": images}
    return render(request, 'api/images.html', context)


def process_group_info(request):
    uuid = request.GET.get('uuid', None)
    if not uuid:
        return HttpResponse('Please send UUID')

    tasks.cluster_pics.apply_async((uuid,))
    return HttpResponse('Processing')


def fetch_group_info(request):
    uuid = request.GET.get('uuid', None)
    if not uuid:
        return HttpResponse('Please send UUID')
    return JsonResponse(elastic.fetch_metadata(uuid))

from models import UploadForm, Upload


# def home(request):
#     print "in API"
#     if request.method == "POST":
#         img = UploadForm(request.POST, request.FILES)
#         if img.is_valid():
#             for imgfile in request.FILES.getlist('image'):
#                 save_file(imgfile, request.POST.get('uuid', 'unnamed'))
#             return HttpResponseRedirect(reverse('imageupload'))
#     else:
#         img = UploadForm()
#     images = Upload.objects.all()
#     return render(request, 'api/home.html', {'form': img, 'images': images})


def index(request):
    uuid = request.GET.get('uuid', 'test')
    MEDIA_ROOT = os.getcwd() + '/images/{}'.format(uuid)
    if not os.path.exists(MEDIA_ROOT):
        os.makedirs(MEDIA_ROOT)
    images = []

    for img in os.listdir(MEDIA_ROOT):
        if img.endswith('crop.jpg'):
            continue
        temp = '../../images/{}/{}'.format(uuid, img)
        images.append(temp)

    if request.method == "POST":
        img = UploadForm(request.POST, request.FILES)
        if img.is_valid():
            for imgfile in request.FILES.getlist('image'):
                save_file(imgfile, request.POST.get('uuid', 'test'))
            return HttpResponseRedirect(reverse('index'))
    else:
        img = UploadForm()
    images_upload = Upload.objects.all()

    groups = elastic.fetch_group_data(uuid)
    print groups

    context = {"images": images, "images_upload": images_upload, 'groups': groups}
    return render(request, 'api/index.html', context)


def search(request):
    print "searching.."
    if request.method == "GET":
        uuid = request.GET.get('uuid', 'test')
        tag = request.GET.get('searchtag', 0)
        try:
            tag = int(tag)
        except:
            pass
        print tag, type(tag)
        images = elastic.fetch_metadata_group(uuid, tag)
        groups = elastic.fetch_group_data(uuid)
        if tag in groups:
            groups = [tag]
        else:
            groups = []
        return render(request, 'api/index.html', {'images': images, "images_upload": [], 'groups': groups})
    else:
        return HttpResponse('Something bad happened')


def update(request):
    group = request.GET.keys()[0]
    newname = request.GET[group]
    json_data = (group, newname)
    elastic.update_metadata(json_data)
    return HttpResponseRedirect(reverse('index'))
