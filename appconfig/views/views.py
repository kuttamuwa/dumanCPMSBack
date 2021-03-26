# Create your views here.
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView
from rest_framework.exceptions import APIException


def app_page(request):
    return render(request, 'main_page.html')


class ImpossibleDecision(APIException):
    status_code = 500
    default_detail = "Gerçekleştirilmesi mümkün olmayan bir işlem denendi !"
    default_code = "NotImplementedError"
