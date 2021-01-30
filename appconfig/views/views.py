# Create your views here.
from django.shortcuts import render
from django.views.generic import DetailView


def app_page(request):
    return render(request, 'main_page.html')
