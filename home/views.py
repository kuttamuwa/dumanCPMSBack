from django.shortcuts import render


# Create your views here.
def main_page(request):
    return render(request, 'main_page.html')


def login_system(request):
    print(request)