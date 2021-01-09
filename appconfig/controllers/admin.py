from django.contrib import admin

# Register your models here.
from appconfig.models.models import Domains, Subtypes

admin.site.register(Domains)
admin.site.register(Subtypes)
