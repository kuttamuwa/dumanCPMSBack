from django.apps import AppConfig

from dumanCPMSRevise.settings import DEBUG


class AppconfigConfig(AppConfig):
    name = 'appconfig'

    @staticmethod
    def import_all_internal_data():
        """
        Domains, subtypes
        :return:
        """
        from appconfig.controllers.hookers import ImportInternalData

        ImportInternalData().import_all()

    @staticmethod
    def import_all_external_data():
        """
        Vergi, SGK vs.
        :return:
        """
        from appconfig.controllers.hookers import ImportExternalData
        ImportExternalData().runforme()

    def ready(self):
        if not DEBUG:
            self.import_all_internal_data()
            self.import_all_external_data()

            print("İç ve Dış verilerin yüklenmesi taranması tamamlandı")