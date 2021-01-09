from django.urls import path, include

from appconfig.views import views
from appconfig.views.routers import router

urlpatterns = [
    path('', views.AppConfigMainView.as_view(), name='appconfig-main'),

    # crud - api
    path('api/', include(router.urls))
]
