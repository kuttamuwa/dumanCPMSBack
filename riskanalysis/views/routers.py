from rest_framework import routers

from dashboard.views.api import RiskAnalysisApi
from riskanalysis.views.api import DatasetAPI, RiskPointsAPI

router = routers.DefaultRouter()

router.register(r'dataset', DatasetAPI)
router.register(r'points', RiskPointsAPI)
# router.register(r'dashboard', RiskAnalysisApi)

