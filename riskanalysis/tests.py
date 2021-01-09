from django.test import TestCase


# Create your tests here.
from riskanalysis.models.models import DataSetModel


class DatasetTests(TestCase):
    @staticmethod
    def test_create_dataset():
        pass

    @staticmethod
    def test_create_datasetv2():
        pass

    @staticmethod
    def calculate_point():
        rd = DataSetModel.objects.all().first()
