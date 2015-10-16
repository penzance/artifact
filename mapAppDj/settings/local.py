from .base import *
from .secure import SECURE_SETTINGS

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += ('debug_toolbar', 'sslserver')

MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

# For Django Debug Toolbar:
INTERNAL_IPS = ('127.0.0.1', '10.0.2.2',)

DEBUG_TOOLBAR_CONFIG = {
   'INTERCEPT_REDIRECTS': False,
}

LOGGING['loggers']['']['level'] = 'DEBUG'
