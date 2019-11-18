from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'get_photo_align_large_files/$', views.get_photo_align_large_files),
    url(r'get_photo_align/$', views.get_photo_align),
    url(r'get_photo_metadata/$', views.get_photo_metadata),
    url(r'get_photo_images/$', views.get_photo_images),
    url(r'get_red_people/$', views.get_red_people),
    url(r'get_photo_red/$', views.get_photo_red),
    url(r'get_photo_redbase/$', views.get_photo_redbase),
]
