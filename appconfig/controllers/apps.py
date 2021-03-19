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
        from appconfig.models.models import Domains, Subtypes
        Domains.import_from_excel()
        Subtypes.import_from_excel()

    @staticmethod
    def import_all_external_data():
        """
        Vergi, SGK vs.
        :return:
        """
        from appconfig.controllers.hookers import ImportExternalData
        try:
            ImportExternalData().runforme()

        except NotImplementedError:
            print("Vergi SGK vs. henüz yüklenemedi. Modül tam değil")

    def ready(self):
        if not DEBUG:
            self.import_all_external_data()
