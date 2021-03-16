from django.db import models

from appconfig.errors.domain.validator import DomainCannotExceeds100
from appconfig.errors.subtype.validator import SubtypeCannotExceeds100
from checkaccount.models.models import CheckAccount


class VergiBorcuManager(models.Manager):
    def get_or_create(self, *args, **kwargs):
        # kwargs['borc_sahibi'] = CheckAccount.dummy_creator.check_or_create_dummy(kwargs['borc_sahibi'])
        return super(VergiBorcuManager, self).get_or_create(*args, **kwargs)

    def create(self, *args, **kwargs):
        return super(VergiBorcuManager, self).create(*args, **kwargs)


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
