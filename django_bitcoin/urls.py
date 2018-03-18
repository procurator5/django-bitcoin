from django.conf.urls import url
from django_bitcoin.views import *

urlpatterns = [
    url(r'^qrcode/(?P<key>.+)$', qrcode_view, name='qrcode'),
]
