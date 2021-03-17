# Create your views here.
from django.shortcuts import render


def checkaccount_page(request):
    return render(request, 'checkaccount_page.html')
