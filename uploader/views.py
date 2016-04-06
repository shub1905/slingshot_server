from django.http import HttpResponse


def index(request):
    if request.method == 'POST':
        print request.FILES.keys()
        save_file(request.FILES['file'])
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
