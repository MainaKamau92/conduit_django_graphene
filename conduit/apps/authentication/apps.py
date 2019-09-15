from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    name = 'conduit.apps.authentication'

    def ready(self):
        from .signals import create_profile