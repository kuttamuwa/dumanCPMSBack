from django.contrib.auth import views
from django.urls import path

from home import views as hviews

urlpatterns = [
    path('', hviews.main_page, name='dcpms-main'),
]
