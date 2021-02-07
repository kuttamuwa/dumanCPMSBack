# Create your views here.
from avatar.models import Avatar
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView


def app_page(request):
    return render(request, 'main_page.html')


def get_avatar(request, username):
    if username not in ('', 'undefined', None):
        usr = User.objects.get(username=username)
        a = Avatar.objects.get(user=usr)

        try:
            with open(a.avatar.file.name, 'rb') as f:
                return HttpResponse(f.read(), content_type='image/jpeg')

        except IOError:
            return HttpResponse('NOT FOUND')

        except ValueError:
            return HttpResponse('NOT FOUND')

    return HttpResponse("NO USERNAME")
