# https://www.liqpay.ua/
from django.conf.global_settings import SESSION_ENGINE, MESSAGE_STORAGE

from shop.settings import INSTALLED_APPS

LIQPAY_PUBLIC_KEY = 'sandbox_i17489931786'
# LIQPAY_PRIVATE_KEY needs to be hidden in a separate ENV file (.env).
LIQPAY_PRIVATE_KEY = 'sandbox_000000000000000000000000000000'
# if there will be true, sandboxed API will be enabled. if false, actual API will be used.
LIQPAY_SANDBOX = True

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400 * 7  # session lasts 7 days upon creation.

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'payments.log',
        },
    },
    'loggers': {
      'products': {
          'handlers': ['console', 'file'],
          'level': 'INFO',
      }
    },
}