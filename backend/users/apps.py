from django.contrib.admin import apps
from django.apps import AppConfig

class UsersConfig(AppConfig): #apps.AdminConfig
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # default_site = 'users.admin.CustomAdminSite'

    def ready(self):
        from . import signals