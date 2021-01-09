from django.db import models

from riskanalysis.models.basemodels import BaseModel


class DummyCreator(models.Manager):
    def generate_dummy_username(self):
        max_value = self.model.objects.all().last().pk
        default_value = self.model.username.field.default
        username = default_value + f"_{max_value}"

        return username

    def create_dummy(self, username=None):
        if username is None:
            username = self.generate_dummy_username()

        return self.create(username=username)


class DummyUser(BaseModel):
    username = models.CharField(max_length=50, default='dummy', unique=True, null=False, blank=True)
    dummy_creator = DummyCreator()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(DummyUser, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.username
