from django.urls import path, include

from home import views

urlpatterns = [
    path('', views.main_page, name='dcpms-main'),
]
