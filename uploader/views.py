from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
# Create your views here.


from models import UploadForm, Upload

def home(request):
    if request.method=="POST":
        img = UploadForm(request.POST, request.FILES)       
        if img.is_valid():
            img.save()  
            return HttpResponseRedirect(reverse('imageupload'))
    else:
        img=UploadForm()
    images=Upload.objects.all()
    return render(request,'home.html',{'form':img,'images':images})


