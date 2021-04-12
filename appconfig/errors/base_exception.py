"""
Uygulamadaki tüm hatalar için base exception sınıfı
"""
from rest_framework.exceptions import APIException


class AppConfigBaseException(APIException):
    default_code = 500
    default_detail = "Uygulama hatası !"

