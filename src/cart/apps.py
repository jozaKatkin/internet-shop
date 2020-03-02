from django.apps import AppConfig


class CartConfig(AppConfig):
    name = 'cart'

    def ready(self):
        # noinspection PyUnresolvedReferences
        from . import signals
