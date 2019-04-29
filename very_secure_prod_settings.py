SECRET_KEY = 'super_secret_key'
DEBUG = False
ALLOWED_HOSTS = ['localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'football_stats',
        'USER': 'some_db_user',
        'PASSWORD': 'some_secure_password',
        'HOST': 'postgres'
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'memcached:11211',
    }
}
