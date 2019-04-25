import os

SECRET_KEY = 'fds@#='
DEBUG = True
ALLOWED_HOSTS = ['localhost']

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': ''
    }
}