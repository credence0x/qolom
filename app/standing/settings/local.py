from .base import *
import os

DEBUG = True

ALLOWED_HOSTS = ['*']


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
                'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.environ.get("LOCAL_POSTGRES_NAME"),
                'USER': os.environ.get("LOCAL_POSTGRES_USER"),
                'PASSWORD': os.environ.get("LOCAL_POSTGRES_PASSWORD"),
                'HOST': f'{os.environ.get("LOCAL_POSTGRES_HOST")}',
                'PORT': '5432',
            }
    }