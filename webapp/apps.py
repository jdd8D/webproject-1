from django.apps import AppConfig
from watson import search as watson


class WebappConfig(AppConfig):
    name = 'webapp'

    def ready(self):
        Technology = self.get_model("Technology")
        watson.register(Technology)