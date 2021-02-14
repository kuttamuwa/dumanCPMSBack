from django.db import models

from appconfig.errors.domain.validator import DomainCannotExceeds100
from appconfig.errors.subtype.validator import SubtypeCannotExceeds100


class PuantageCreateManager(models.Manager):
    point_field = 'point'
    raise_state = None

    def validate(self):
        self.check_points()

    def _get_cannot_exceeds_exception(self):
        pass

    def check_points(self):
        values = self.values(self.point_field)
        if sum(values) > 100:
            raise self._get_cannot_exceeds_exception()


class DomainCreateManager(PuantageCreateManager):
    def _get_cannot_exceeds_exception(self):
        return DomainCannotExceeds100


class SubtypeCreateManager(PuantageCreateManager):
    def _get_cannot_exceeds_exception(self):
        return SubtypeCannotExceeds100


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
    pass

