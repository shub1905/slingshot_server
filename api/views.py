from django.http import HttpResponse
from django.http import JsonResponse
from api.elasticsearchModel import elastic
import tasks
import uuid
import json
import os


def userid(request):
    response_data = {}
    response_data['uuid'] = uuid.uuid1()
    response_data['message'] = 'This is the unique user id'
    return JsonResponse(response_data)


def upload(request):
    if request.method == 'POST':
        save_file(request.FILES['image'], request.POST.get('uuid', 'unnamed'))
        # elastic.save_metadata(request.POST)
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


def fetch_group_info(request, uuid):
    image_ids = json.loads(request.GET['image_ids'])
    print image_ids
    response = elastic.fetch_metadata(image_ids)
    return JsonResponse(response)
