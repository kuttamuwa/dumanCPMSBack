from django.urls import path, include

from home import views

urlpatterns = [
    path('', views.main_page, name='dcpms-main'),
    path('login/<str:username>', views.login_system, name='dcpms-login')
]
