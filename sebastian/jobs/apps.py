from django.apps import AppConfig

class JobsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "jobs"
    
    def ready(self):
        """
        This function is called when startup.
        """
        from .scheduler import start
        start()
