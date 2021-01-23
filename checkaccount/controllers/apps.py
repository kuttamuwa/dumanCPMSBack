from django.apps import AppConfig


class CheckaccountConfig(AppConfig):
    name = 'checkaccount'

    @staticmethod
    def import_il_ilce():
        # il ilçe yükleme
        from checkaccount.controllers.hookers import ImportCityDistrict
        ImportCityDistrict().test_runforme()

    @staticmethod
    def import_sys_personnels():
        from checkaccount.controllers.hookers import ImportPersonnels
        ImportPersonnels().test_runforme()

    def ready(self):
        self.import_il_ilce()
        self.import_sys_personnels()
