from rest_framework import routers

from riskanalysis.views.api import DatasetAPI, RiskPointsAPI, DatasetExAPI, CardsAPI

router = routers.DefaultRouter(trailing_slash=True)

router.register(r'dataset', DatasetAPI)
# router.register(r'datasetex', DatasetExAPI)
router.register(r'points', RiskPointsAPI)
router.register(r'dashboard', CardsAPI, basename='dashboard')
