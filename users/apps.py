from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        # Import signals to ensure they are registered when the app is ready
        import users.signals
        # This will ensure that the signals are connected when the app is loaded
