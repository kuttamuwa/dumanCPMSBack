from django.urls import path, include

from checkaccount.views import views
from checkaccount.views.routers import router

urlpatterns = [
    path('', views.checkaccount_page, name='checkaccout-main'),

    # crud - api
    path('api/', include(router.urls))
]
