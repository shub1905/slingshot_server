from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'upload/$', views.upload, name='upload'),
    url(r'celery/$', views.celery_test, name='celery_test'),
    url(r'userid/$', views.userid, name='userid'),
]