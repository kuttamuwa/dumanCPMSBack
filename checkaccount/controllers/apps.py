from django.apps import AppConfig

from dumanCPMSRevise.settings import DEBUG


class CheckaccountConfig(AppConfig):
    name = 'checkaccount'

    @staticmethod
    def import_il_ilce():
        # il ilçe yükleme
        from checkaccount.controllers.hookers import ImportCityDistrict
        ImportCityDistrict().runforme()
        print("İl ilçe verisi yüklendi ")

    @staticmethod
    def import_sys_personnels():
        from checkaccount.controllers.hookers import ImportPersonnels
        ImportPersonnels().runforme()
        print("Sistem personelleri yüklendi")

    @staticmethod
    def import_account_data():
        from checkaccount.controllers.hookers import ImportAccounts
        ImportAccounts().runforme()
        print("Cari hesaplar yüklendi")

    @staticmethod
    def import_sector_data():
        from checkaccount.controllers.hookers import ImportSectors
        ImportSectors().runforme()
        print("Sektör listesi yüklendi ")

    def ready(self):
        if not DEBUG:
            self.import_il_ilce()
            self.import_sys_personnels()
            self.import_sector_data()
            self.import_account_data()

            print("Check account uygulaması ve test verileri yüklendi")