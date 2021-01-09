# Create your views here.
from django.views.generic import DetailView


class RiskDatasetMainView(DetailView):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass
