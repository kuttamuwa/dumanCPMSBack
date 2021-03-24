from rest_framework import routers

from riskanalysis.views.api import DatasetAPI, RiskPointsAPI, DatasetExAPI

router = routers.DefaultRouter()

router.register(r'dataset', DatasetAPI)
router.register(r'datasetex', DatasetExAPI)
router.register(r'points', RiskPointsAPI)
# router.register(r'dashboard', RiskAnalysisApi)

