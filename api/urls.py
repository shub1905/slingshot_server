from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'upload/$', views.upload, name='upload'),
    url(r'userid/$', views.userid, name='userid'),
    url(r'process/$', views.process_group_info, name='process_group_info'),
    url(r'fetch/$', views.fetch_group_info, name='fetch_group_info'),
    url(r'upload2/$', views.home, name='imageupload'),

]
