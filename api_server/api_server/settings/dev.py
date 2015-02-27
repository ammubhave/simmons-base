from base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ws&-!e*vw*8oi908_*f(=-dt6_jrhh*p$_hy*@043muq@kq4_r'

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

INSTALLED_APPS = INSTALLED_APPS + [
    'debug_toolbar',
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
