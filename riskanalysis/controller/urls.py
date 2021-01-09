from django.urls import path, include

from riskanalysis.views import views
from riskanalysis.views.routers import router

urlpatterns = [
    path('', views.RiskDatasetMainView.as_view(), name='riskanalysis-main'),

    # crud - api
    path('api/', include(router.urls))
]
