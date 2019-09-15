from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    name = 'conduit.apps.articles'

    def ready(self):
        from .signals import add_slug_to_article_if_not_exists
