from django.conf import settings
from django.db import models


class BaseModel(models.Model):
    # objects = models.Manager
    data_id = models.AutoField(primary_key=True)

    created_date = models.DateTimeField(auto_now_add=True,
                                        verbose_name='Created Date',)

    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
    #                                on_delete=models.SET_NULL, verbose_name='Created by',
    #                                related_name='BaseCreatedBy')

    # edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'RISK_BASEMODEL'
