# Create your views here.
#from avatar.models import Avatar
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView


def app_page(request):
    return render(request, 'main_page.html')


