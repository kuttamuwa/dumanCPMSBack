import os

import pandas as pd
from django.db import models

from appconfig.models.basemodels import BaseModel


# Create your models here.
# Puantage #

class Domains(BaseModel):
    name = models.CharField(db_column='DOMAIN', max_length=100, unique=True, null=False)
    point = models.FloatField(max_length=100, default=0.0, db_column='POINT',
                              help_text='Set your domain point of your variable',
                              unique=False, null=False)

    @staticmethod
    def import_from_excel():
        path = os.path.abspath(r'.\appconfig\data\Domains.xlsx')
        df = pd.read_excel(path)

        for index, row in df.iterrows():
            name = row['name']
            point = row['point']

            d = Domains(name=name, point=point)
            d.save()

    def __str__(self):
        return f'Domain: {self.name} \n' \
               f'General Point : {self.point}'

    class Meta:
        db_table = 'DOMAINS'


class Subtypes(BaseModel):
    domain = models.ForeignKey(Domains, on_delete=models.SET_NULL, max_length=100)

    point = models.FloatField(max_length=100, db_column='PTS', help_text='Point of specified intervals '
                                                                         'of your subtype related Domain')
    min_interval = models.FloatField(max_length=100, db_column='MIN_INTERVAL', help_text='Minimum interval')

    max_interval = models.FloatField(max_length=100, db_column='MAX_INTERVAL', help_text='Maximum interval',
                                     blank=True, null=True)

    @staticmethod
    def import_from_excel():
        path = os.path.abspath(r'.\appconfig\data\Subtypes.xlsx')
        df = pd.read_excel(path)

        for index, row in df.iterrows():
            domain_name = row['domain_name']
            d = Domains.objects.get(name=domain_name)
            point = row['point']
            min_interval = row['min_interval']
            max_interval = row['max_interval']

            s = Subtypes(domain=d, min_interval=min_interval, max_interval=max_interval,
                         point=point)
            s.save()

    def __str__(self):
        return f"Points of {self.domain} : \n" \
               f"Minimum interval: {self.min_interval} \n" \
               f"Maximum interval: {self.max_interval}"

    class Meta:
        db_table = 'SUBTYPES'
