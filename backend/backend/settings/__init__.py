from .base import *

environment = os.environ.get('DJANGO_ENV')

if environment == 'production':
    from .production import *
else:
    from .development import *