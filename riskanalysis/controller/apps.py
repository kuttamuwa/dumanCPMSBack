from django.apps import AppConfig

from dumanCPMSRevise.settings import DEBUG


class RiskanalysisConfig(AppConfig):
    name = 'riskanalysis'

    @staticmethod
    def import_test_data():
        from riskanalysis.controller.hookers import ImportRiskDataset
        ImportRiskDataset().runforme()

    def ready(self):
        if not DEBUG:
            self.import_test_data()
