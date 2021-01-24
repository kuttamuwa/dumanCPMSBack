from django.apps import AppConfig


class AppconfigConfig(AppConfig):
    name = 'appconfig'

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
        self.import_all_external_data()
