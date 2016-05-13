from __future__ import unicode_literals

from django.db import models
from django.forms import ModelForm


class Upload(models.Model):
    image = models.ImageField("Image", upload_to="images/")    
    upload_date=models.DateTimeField(auto_now_add =True)
    uuid = 123

# FileUpload form class.
class UploadForm(ModelForm):
    class Meta:
        model = Upload
        fields = '__all__'