from django.apps import AppConfig

class YourappnameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

   # apps.py
def ready(self):
    import myapp.signals