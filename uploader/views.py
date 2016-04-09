from django.http import HttpResponse
import tasks

def index(request):
    if request.method == 'POST':
        save_file(request.FILES['image'])
        return HttpResponse('Thanks for uploading the image')
    return HttpResponse('Something bad happened')


def save_file(file, path=''):
    ''' Little helper to save a file
    '''
    MEDIA_ROOT = '.'
    filename = file._get_name()
    fd = open('%s/%s' % (MEDIA_ROOT, str(path) + str(filename)), 'wb')
    for chunk in file.chunks():
        fd.write(chunk)
    fd.close()

def celery_test(request):
    for i in range(1000):
        tasks.mul.apply_async(4,5)