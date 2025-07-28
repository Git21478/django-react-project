from django.contrib.admin import apps
from django.apps import AppConfig

class ProductsConfig(AppConfig): #apps.AdminConfig
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    def ready(self):
        from . import signals