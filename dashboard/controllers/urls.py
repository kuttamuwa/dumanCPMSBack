from django.urls import path, include

from dashboard.views import views
from dashboard.views.routers import router

urlpatterns = [
    path('', views.dashboard_page, name='checkaccout-main'),

    # crud - api
    path('api/', include(router.urls))
]
