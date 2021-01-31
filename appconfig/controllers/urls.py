from django.urls import path, include

from appconfig.views import views
from appconfig.views.routers import router

urlpatterns = [
    path('', views.app_page, name='appconfig-main'),

    # crud - api
    path('api/', include(router.urls)),

    path('avatars/', include('avatar.urls')),
    path('getavatar/<str:username>', views.get_avatar, name='get-avatar')
]
