"""dumanCPMSRevise URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from appconfig.utils.perms import getperms

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),

    # authentication on rest framework with JWT
    path('auth/login/', obtain_jwt_token),
    path('auth/refresh-token/', refresh_jwt_token),
    path('auth/verify-token/', verify_jwt_token),

    path('auth/getperms', getperms),

    path('', include('home.urls')),

    path('appconfig/', include('appconfig.controllers.urls')),

    # modules
    path('checkaccount/', include('checkaccount.controllers.urls')),
    path('riskanalysis/', include('riskanalysis.controller.urls')),
    path('dashboard/', include('dashboard.controllers.urls')),
]
