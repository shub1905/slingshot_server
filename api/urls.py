from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'upload/$', views.upload, name='upload'),
    url(r'userid/$', views.userid, name='userid'),
    url(r'info/$', views.fetch_group_info, name='groupinfo'),
]