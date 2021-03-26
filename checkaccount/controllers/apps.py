from django.apps import AppConfig

from dumanCPMSRevise.settings import DEBUG


class CheckaccountConfig(AppConfig):
    name = 'checkaccount'

    @staticmethod
    def import_il_ilce():
        # il ilçe yükleme
        from checkaccount.controllers.hookers import ImportCityDistrict
        ImportCityDistrict().runforme()

    @staticmethod
    def import_sys_personnels():
        from checkaccount.controllers.hookers import ImportPersonnels
        ImportPersonnels().test_runforme()

    @staticmethod
    def import_account_data():
        from checkaccount.controllers.hookers import ImportAccounts
        ImportAccounts().test_runforme()

    @staticmethod
    def import_sector_data():
        from checkaccount.controllers.hookers import ImportSectors
        ImportSectors().test_runforme()

    def ready(self):
        if not DEBUG:
            self.import_il_ilce()
            self.import_sys_personnels()
            self.import_account_data()
            self.import_sector_data()