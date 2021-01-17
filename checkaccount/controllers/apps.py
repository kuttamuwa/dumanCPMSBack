from django.apps import AppConfig

from checkaccount.controllers.hookers import ImportCityDistrict


class CheckaccountConfig(AppConfig):
    name = 'checkaccount'

    def ready(self):
        # il ilçe yükleme
        ImportCityDistrict().test_runforme()

