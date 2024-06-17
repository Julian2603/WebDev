# useractivitylogs/apps.py

from django.apps import AppConfig

class UserActivityLogsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'useractivitylogs'

    def ready(self):
        import useractivitylogs.signals
