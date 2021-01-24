from rest_framework import routers

from riskanalysis.views.api import DatasetAPI, RiskPointsAPI

router = routers.DefaultRouter()

router.register(r'dataset', DatasetAPI)
router.register(r'points', RiskPointsAPI)
# router.register(r'pointsv2', RiskPointsAPIv2.as_view())
