from django.conf import settings
from django.db import models
import os
import pandas as pd

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


"""
Aşağıyı kaldırıyorum. Sebebi:
Excel'in sütunlarını güncellemek, uygulamada eşleşme oluşturmaktan daha kolay
"""

# class RiskDataConfigModel(models.Model):
#     # CUSTOMER = 0
#     # LIMIT = 1
#     # WARRANT_STATE = 2
#     # WARRANT_AMOUNT = 3
#     # MATURITY = 4
#     # MATURITY_EXCEED_AVG = 5
#     # AVG_ORDER_AMOUNT_LAST_TWELVE_MONTHS = 6
#     # AVG_ORDER_AMOUNT_LAST_THREE_MONTHS = 7
#     # LAST_3_MONTHS_ABERRATION = 8
#     # LAST_MONTH_PAYBACK_PERC = 9
#     # LAST_TWELVE_MONTHS_PAYBACK_PERC = 10
#     # LAST_THREE_MONTHS_PAYBACK_COMPARISON = 11
#     # AVG_LAST_THREE_MONTHS_PAYBACK_PERC = 12
#     # AVG_DELAY_TIME = 13
#     # AVG_DELAY_BALANCE = 14
#     # PERIOD_DAY = 15
#     # PERIOD_VELOCITY = 16
#     # RISK_EXCLUDED_WARRANT_BALANCE = 17
#     # BALANCE = 18
#     # PROFIT = 19
#     # PROFIT_PERCENT = 20
#     # TOTAL_RISK_INCLUDING_CHEQUE = 21
#     # LAST_12_MONTHS_TOTAL_ENDORSEMENT = 22
#
#     # source fields
#     SOURCE_FIELD_CHOICES = (
#          ('CUSTOMER', 'Müşteri'),
#          ('LIMIT', 'Limit'),
#          ('WARRANT_STATE', 'Teminat Durumu'),
#          ('WARRANT_AMOUNT', 'Teminat Tutarı'),
#          ('MATURITY', 'Vade'),
#          ('MATURITY_EXCEED_AVG', 'Ortalama Gecikme Gün Bakiyesi'),
#          ('AVG_ORDER_AMOUNT_LAST_TWELVE_MONTHS', 'Son 12 Ay Ortalama Sipariş Tutarı'),
#          ('AVG_ORDER_AMOUNT_LAST_THREE_MONTHS', 'Son 3 Ay Ortalama Sipariş Tutarı'),
#          ('LAST_3_MONTHS_ABERRATION',
#           'Son 3 ay ile son 11 aylık satış ortalamasından sapma'),
#          ('LAST_MONTH_PAYBACK_PERC', 'Son ay iade yuzdesi'),
#          ('LAST_TWELVE_MONTHS_PAYBACK_PERC', 'Son 12 ay iade yüzdesi'),
#          ('LAST_THREE_MONTHS_PAYBACK_COMPARISON',
#           'Son 3 ay ile son 11 aylık iade yüzdesi karşılaştırması'),
#          ('AVG_LAST_THREE_MONTHS_PAYBACK_PERC', 'Son 3 ay iade yuzdesi'),
#          ('AVG_DELAY_TIME', 'Ortalama gecikme gün sayısı'),
#          ('AVG_DELAY_BALANCE', 'Ortalama gecikme gün bakiyesi'),
#          ('PERIOD_DAY', 'Devir günü'),
#          ('PERIOD_VELOCITY', 'Devir hızı'),
#          ('RISK_EXCLUDED_WARRANT_BALANCE', 'Teminat harici bakiye - risk'),
#          ('BALANCE', 'Bakiye'),
#          ('PROFIT', 'Kar'),
#          ('PROFIT_PERCENT', 'Kar yüzdesi'),
#          ('TOTAL_RISK_INCLUDING_CHEQUE', 'Çek dahil toplam risk'),
#          ('LAST_12_MONTHS_TOTAL_ENDORSEMENT', 'Son 12 aylık toplam ciro')
#     )
#     source_field = models.CharField(max_length=100, help_text='Kaynak veri ismi',
#                                     choices=SOURCE_FIELD_CHOICES)
#     target_field = models.CharField(max_length=100, help_text='Exceldeki sütun ismi')
