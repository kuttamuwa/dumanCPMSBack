from django.apps import AppConfig


class CheckaccountConfig(AppConfig):
    name = 'checkaccount'

    def ready(self):
        # il ilçe yükleme
        from checkaccount.controllers.hookers import ImportCityDistrict
        ImportCityDistrict().test_runforme()
