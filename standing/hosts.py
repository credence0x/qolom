from django_hosts import patterns,host
from django.conf import settings



host_patterns = patterns('',
    host(r'www', settings.ROOT_URLCONF, name='www'),
    host(r'admin','standing.adminurl',name='admin'),
    host(r'media','logos.urls',name='media'),
)
