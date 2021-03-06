from django.apps import AppConfig


class RiskanalysisConfig(AppConfig):
    name = 'riskanalysis'

    @staticmethod
    def import_test_data():
        from riskanalysis.tests.tests import RiskDatasetTests
        RiskDatasetTests().test_runforme()

    def ready(self):
        self.import_test_data()
