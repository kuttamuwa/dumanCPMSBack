from django.db import models
from django.conf import settings


class BaseModel(models.Model):
    data_id = models.AutoField(primary_key=True)

    created_date = models.DateTimeField(auto_now_add=True, db_column='CREATED_DATE',
                                        verbose_name='Created Date')

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                   on_delete=models.SET_NULL, verbose_name='Created by')

    class Meta:
        abstract = True
        db_table = 'CA_BASEMODEL'
        ordering = ['created_date']

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(BaseModel, self).save(force_insert, force_update, using, update_fields)

