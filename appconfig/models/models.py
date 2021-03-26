import os

import pandas as pd
from django.db import models

from appconfig.models.basemodels import BaseModel

# Create your models here.
# Puantage #
from appconfig.models.managers import VergiBorcuManager
from checkaccount.models.models import CheckAccount
from dumanCPMSRevise.settings import BASE_DIR


class Domains(BaseModel):
    name = models.CharField(db_column='DOMAIN', max_length=100, unique=True, null=False)
    point = models.FloatField(max_length=100, default=0.0, db_column='POINT',
                              help_text='Set your domain point of your variable',
                              unique=False, null=False)

    def __str__(self):
        return f'Domain: {self.name} \n' \
               f'General Point : {self.point}'

    class Meta:
        db_table = 'DOMAINS'


class Subtypes(BaseModel):
    domain = models.ForeignKey(Domains, on_delete=models.CASCADE, max_length=100)

    point = models.FloatField(max_length=100, db_column='PTS', help_text='Point of specified intervals '
                                                                         'of your subtype related Domain')
    min_interval = models.FloatField(max_length=100, db_column='MIN_INTERVAL', help_text='Minimum interval')

    max_interval = models.FloatField(max_length=100, db_column='MAX_INTERVAL', help_text='Maximum interval',
                                     blank=True, null=True)

    def __str__(self):
        return f"Points of {self.domain} : \n" \
               f"Minimum interval: {self.min_interval} \n" \
               f"Maximum interval: {self.max_interval}"

    class Meta:
        db_table = 'SUBTYPES'


# Vergi SGK ıvır zıvır

class BaseBlackLists(BaseModel):
    borc_sahibi = models.CharField(unique=False,
                                   help_text='Borçlunun Adı Soyadı',
                                   db_column='DEPT_TITLE', max_length=250, null=True)

    # borc_sahibi = models.CharField(unique=False,
    #                                help_text='Borçlunun Adı Soyadı',
    #                                db_column='DEPT_TITLE', max_length=150, null=True)

    class Meta:
        db_table = 'BLACK_LIST'
        abstract = True

    def __str__(self):
        return f"Black list for : {self.borc_sahibi}"


class SGKBorcuListesi(BaseBlackLists):
    kimlikno = models.CharField(unique=False, help_text='Sahis firmasi ise TCKNO, Tuzel Kisilik ise'
                                                        'Vergi No',
                                db_column='TAXPAYER_NUMBER', max_length=15)
    borc_miktari = models.FloatField(unique=False,
                                     help_text='Borç Miktarı',
                                     db_column='DEPT_AMOUNT')

    class Meta:
        db_table = 'SGK_DEBTS'

    def __str__(self):
        return f"SGK Debts for {self.borc_sahibi}"


class VergiBorcuListesi(BaseBlackLists):
    vergi_departmani = models.CharField(max_length=200, verbose_name='TAX DEPARTMENT',
                                        db_column='TAX_DEPT', unique=False,
                                        help_text='Vergi Departmanı')
    esas_faaliyet_konusu = models.CharField(unique=False,
                                            help_text='Esas Faaliyet Konusu',
                                            db_column='REAL_OPERATING_INCOME', max_length=500)
    borc_miktari = models.FloatField(unique=False,
                                     help_text='Borç Miktarı',
                                     db_column='DEPT_AMOUNT')
    borc_sahibi = models.ForeignKey(CheckAccount, on_delete=models.CASCADE)

    objects = VergiBorcuManager()

    class Meta:
        db_table = 'TAX_DEBTS'

    def __str__(self):
        return f"Tax Debts for  {self.borc_sahibi}"


class SystemBlackList(BaseBlackLists):
    class Meta:
        db_table = 'SYS_BLACK_LIST'

    def __str__(self):
        return 'System Black List'


class KonkordatoList(BaseBlackLists):
    class Meta:
        db_table = 'KONKORDATO_LIST'

    def __str__(self):
        return 'Konkordato Black List'
