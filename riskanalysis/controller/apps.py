from django.apps import AppConfig


class RiskanalysisConfig(AppConfig):
    name = 'riskanalysis'

    @staticmethod
    def import_test_data():
        from riskanalysis.controller.hookers import ImportRiskDataset
        ImportRiskDataset().test_runforme()

    def ready(self):
        # todo: set
        # if not DEBUG:
        self.import_test_data()
