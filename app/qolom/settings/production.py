from .base import *
import os

DEBUG = os.environ.get("DJANGO_DEBUG")

# FOR DEMONSTRATION ONLY
ALLOWED_HOSTS = ['*'] 



# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
            'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get("POSTGRES_NAME"),
            'USER': os.environ.get("POSTGRES_USER"),
            'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
            'HOST': f'{os.environ.get("POSTGRES_HOST")}',
            'PORT': '5432',
        }
}