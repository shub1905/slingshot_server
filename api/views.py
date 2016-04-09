from django.http import HttpResponse
from django.http import JsonResponse
from api.elasticsearchModel import elastic
import tasks
import uuid
import os

def userid(request):
    response_data = {}
    response_data['uuid'] = uuid.uuid1()
    response_data['message'] = 'This is the unique user id'
    return JsonResponse(response_data)


def upload(request):
    if request.method == 'POST':
        save_file(request.FILES['image'], request.POST.get('uuid', 'unnamed'))
        elastic.save_metadata(request.POST)
        tasks.process_image.apply_async((userid, ))
        return HttpResponse('Thanks for uploading the image')
    return HttpResponse('Something bad happened')


def save_file(file, uuid):
    ''' Little helper to save a file
    '''
    MEDIA_ROOT = 'images/'+uuid
    if not os.path.exists(MEDIA_ROOT):
        os.makedirs(MEDIA_ROOT)
    filename = file._get_name()
    fd = open('%s/%s' % (MEDIA_ROOT, str(filename)), 'wb')
    for chunk in file.chunks():
        fd.write(chunk)
    fd.close()