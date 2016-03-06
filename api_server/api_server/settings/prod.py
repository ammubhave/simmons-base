from base import *

# SECURITY WARNING: keep the secret key used in production secret!
with open(os.path.join(EXTERNAL_CONFIG, 'secret_key'), 'r') as f:
    SECRET_KEY = f.read().strip()

# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['simmons-dev.mit.edu', 'simmons.mit.edu']

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
with open(os.path.join(EXTERNAL_CONFIG, 'api_db_password'), 'r') as f:
    _db_password = f.read().strip()
with open(os.path.join(EXTERNAL_CONFIG, 'api_sdb_password'), 'r') as f:
    _sdb_password = f.read().strip()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'simdb',
        'USER': 'api',
        'PASSWORD': _db_password,
        'HOST': '127.0.0.1',
        'PORT': 5432,
    },
    'sdb': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sdb',
        'USER': 'api',
        'PASSWORD': _sdb_password,
        'HOST': 'simmons.mit.edu',#:'seagull.mit.edu',
        'PORT': 5432,
    },
    'scripts_rooming': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'simmons-hall+rooming1',
        'OPTIONS': {
            'read_default_file' : os.path.join(EXTERNAL_CONFIG, 'scripts.my.cnf'),
        },
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
}

DATABASE_ROUTERS = ['api_server.sdb_utils.SdbRouter']

MIDDLEWARE_CLASSES = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'auth.middleware.SimmonsAuthMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

INTERNAL_IPS = ('2001:4830:2446:60:2289:84ff:fed3:d286','127.0.0.1',)
def show_toolbar(request):
    return True
SHOW_TOOLBAR_CALLBACK = show_toolbar

INSTALLED_APPS = INSTALLED_APPS + [
    'debug_toolbar',
]

STATIC_URL = '/api/static/'

AUTHENTICATION_BACKENDS = ('auth.backend.SimmonsAuthBackend','oauth2_provider.backends.OAuth2Backend')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/httpd/api_server_django.log',
        },
    },
    'loggers': {
        'api_server': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}

CORS_ORIGIN_REGEX_WHITELIST = ("""^(https?://)?(\w+\.)?simmons(-dev)?\.mit\.edu$""", """^(https?://)?localhost(:\d+)?$""")

LOGIN_URL = '/api/admin/login/'
