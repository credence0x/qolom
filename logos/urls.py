from django.urls import re_path
from .views import my_image

urlpatterns = [
    re_path(r'^(?P<image>[-\w\s\d.]+)/$', my_image, name='image'),
]
