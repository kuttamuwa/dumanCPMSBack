# Create your views here.
from django.shortcuts import render


def riskanalysis_page(request):
    return render(request, 'riskanalysis_page.html')
