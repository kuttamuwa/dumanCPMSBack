from django.db import models


class DummyCreator(models.Manager):
    def generate_dummy_username(self, **kwargs):
        max_value = kwargs.get('number')
        default_value = self.model.firm_full_name.field.default

        if max_value is None:
            if len(self.model.objects.all()) == 0:
                max_value = 0
            else:
                max_value = self.model.objects.all().last().pk + 1

        username = default_value + f"_{max_value}"

        return username

    def create_dummy(self, username=None, **kwargs):
        if username is None:
            username = self.generate_dummy_username(**kwargs)

        return self.create(firm_full_name=username)


class DummyCheckAccountCreator(DummyCreator):
    def check_or_create_dummy(self, adsoyad):
        try:
            return self.get(firm_full_name=adsoyad)
        except models.ObjectDoesNotExist:
            return self.create_dummy(username=adsoyad)