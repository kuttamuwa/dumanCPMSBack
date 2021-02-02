import numpy as np
import pandas as pd
from django.db import models

from riskanalysis.errors.validators import BalanceError, NoImplementedParameter
from riskanalysis.models.basemodels import BaseModel
from riskanalysis.models.managers import RiskDataSetManager, AnalyzeManager

"""
:exception: Şu anda Customer sütunu CheckAccount üzerinden gelmektedir. 
Check Account modülü satılmayacaksa aşağıdan DummyUser olarak gösterilmesi gerekir

"""

from checkaccount.models.models import CheckAccount


class DataSetModel(BaseModel):
    objects = RiskDataSetManager()

    musteri = models.ForeignKey(CheckAccount, on_delete=models.PROTECT, verbose_name='İlişkili Müşteri',
                                null=True, blank=True, db_column='CUSTOMER')

    limit = models.PositiveIntegerField(db_column='LIMIT', null=True, verbose_name='Limit', blank=True)  # 500 0000 vs

    # teminat
    teminat_durumu = models.BooleanField(db_column='TEMINAT_DURUMU', help_text='Teminat durumu',
                                         null=True, default=False, verbose_name='Teminat Durumu', blank=True)  # var yok
    teminat_tutari = models.PositiveIntegerField(db_column='TEMINAT_TUTARI', help_text='Teminat Tutarı',
                                                 null=True, verbose_name='Teminat Tutarı', blank=True)  # 500 000 vs

    # vade ve odeme
    vade = models.IntegerField(db_column='VADE_GUNU', help_text='Vade Günü', null=True, blank=True,
                               verbose_name='Vade Günü')  # gun
    vade_asimi_ortalamasi = models.IntegerField(db_column='ORT_VADE_ASIMI',
                                                help_text='Vade aşımı ortalaması giriniz', null=True, blank=True,
                                                verbose_name='Vade aşımı ortalaması')
    odeme_sikligi = models.IntegerField(db_column='ODEME_SIKLIGI', help_text='Ödeme sıklığı', null=True, blank=True,
                                        verbose_name='Ödeme sıklığı')

    # Sipariş tutarları
    ort_siparis_tutari_12ay = models.FloatField(db_column='ORT_SIPARIS_TUTARI_12',
                                                help_text='Son 12 ay ortalama sipariş tutarı',
                                                null=True, verbose_name='Son 12 Ay Ortalama Sipariş Tutarı',
                                                blank=True)
    ort_siparis_tutari_1ay = models.FloatField(db_column='ORT_SIPARIS_TUTARI_1', blank=True,
                                               help_text='Son 1 ay ortalama sipariş tutarı',
                                               null=True, verbose_name='Son 1 Ay Ortalama Sipariş Tutarı')

    # iade yüzdeleri
    iade_yuzdesi_1 = models.PositiveSmallIntegerField(db_column='PAYBACK_PERC_LAST',
                                                      help_text='Son ay iade yuzdesi',
                                                      null=True, verbose_name='Son ay iade yüzdesi',
                                                      blank=True)
    iade_yuzdesi_12 = models.FloatField(db_column='PAYBACK_PERC_12', blank=True,
                                        help_text='Son 12 ay iade yüzdesi',
                                        null=True, verbose_name='Son 12 ay iade yüzdesi')

    # gecikmeler
    ort_gecikme_gun_sayisi = models.SmallIntegerField(db_column='AVG_DELAY_TIME', help_text='Ort gecikme gun sayisi',
                                                      null=True,
                                                      verbose_name='Ortalama gecikme gün sayısı', blank=True)

    ort_gecikme_gun_bakiyesi = models.IntegerField(db_column='MATURITY_EXCEED_AVG',
                                                   help_text='Ortalama gecikme gun bakiyesi',
                                                   verbose_name='Ortalama Gecikme Gün Bakiyesi', blank=True,
                                                   null=True)  # gun

    bakiye = models.PositiveIntegerField(db_column='BALANCE', blank=True, help_text='Bakiye', null=True,
                                         verbose_name='Bakiye')

    # will be calculated later with analyzer service
    general_point = models.FloatField(verbose_name='Genel Puan', null=True, blank=True,
                                      db_column='GENERAL_POINT')

    def __str__(self):
        return f"Risk Dataset: {self.musteri}"

    """
    Devir günü
    Devir hızı
    Teminat harici bakiye - risk
    Son 1 - 11 satış ort. sapma karşılaştırması
    Son 1 - 11 iade yüzdesi karşılaştırması
    """

    def read_from_excel(self, riskdataset_path):
        try:
            df = pd.read_excel(riskdataset_path)
            return self._save(df)
        except IOError as err:
            # dosya silinmis olabilir? o kisa sure icerisinde kim silecek gerci?
            raise err

        except KeyError as err:
            # dogru sutunlar girilmemis olabilir
            raise err

    @staticmethod
    def _save(df):
        df.replace(np.nan, None, inplace=True)
        for index, row in df.iterrows():
            musteri = row['Müşteri']
            limit = row['Limit']

            # teminat
            teminat_durumu = row['Teminat Durumu']
            teminat_tutari = row['Teminat Tutarı']

            # vade ve odeme
            vade = row['Vade']
            vade_asimi_ortalamasi = row.get('Ort. Vade Aşımı', None)
            odeme_sikligi = row.get('Ödeme Sıklığı', None)

            # Sipariş tutarlar
            ort_siparis_tutari_12ay = row['Son 12 Ay Ortalama Sipariş Tutarı']
            ort_siparis_tutari_1ay = row['Son 1 Ay Ortalama Sipariş Tutarı']

            # iade yüzdeleri
            iade_yuzdesi_1 = row.get('Son 1 ay iade yüzdesi', None)
            iade_yuzdesi_12 = row['Son 12 ay iade yüzdesi']

            # gecikmeler
            ort_gecikme_gun_sayisi = row['Ort. Gecikme Gün Sayısı']
            ort_gecikme_gun_bakiyesi = row['Ort. Gecikme Gün Bakiyesi (TL)']

            bakiye = row.get('Bakiye')
            DataSetModel.objects.get_or_create(musteri=musteri, limit=limit, teminat_durumu=teminat_durumu,
                                               teminat_tutari=teminat_tutari,
                                               vade=vade, vade_asimi_ortalamasi=vade_asimi_ortalamasi,
                                               odeme_sikligi=odeme_sikligi,
                                               ort_siparis_tutari_1ay=ort_siparis_tutari_1ay,
                                               ort_siparis_tutari_12ay=ort_siparis_tutari_12ay,
                                               iade_yuzdesi_1=iade_yuzdesi_1,
                                               iade_yuzdesi_12=iade_yuzdesi_12,
                                               ort_gecikme_gun_sayisi=ort_gecikme_gun_sayisi,
                                               ort_gecikme_gun_bakiyesi=ort_gecikme_gun_bakiyesi,
                                               bakiye=bakiye
                                               )

        return True

    @staticmethod
    def x_y_z(x, y):
        value = None
        if x is not None and y is not None:
            value = ((x - y) / y) * 100

        return value

    def hesapla_karsilastir_teminat_limit(self):
        if self.teminat_durumu:
            return (self.teminat_tutari / self.limit) * 100
        else:
            return 0

    def hesapla_devir_gunu(self):
        devir_hizi = self.hesapla_devir_hizi()
        return 30 // devir_hizi

    def hesapla_teminatharicibakiye_risk(self):
        return self.bakiye - self.teminat_tutari

    def hesapla_devir_hizi(self, ay=1):
        if ay == 12:
            siparis_tutari = self.ort_siparis_tutari_12ay

        elif ay == 1:
            siparis_tutari = self.ort_siparis_tutari_1ay

        else:
            raise NoImplementedParameter

        if self.bakiye is None:
            raise BalanceError

        if self.ort_siparis_tutari_1ay is None:
            raise BalanceError

        return siparis_tutari / self.bakiye

    def hesapla_analiz_karari(self):
        decision = False
        if self.iade_yuzdesi_12 and self.ort_siparis_tutari_12ay and self.iade_yuzdesi_1:
            if self.ort_siparis_tutari_12ay * 0.1 <= self.iade_yuzdesi_1:
                decision = True

        # todo: Bunu mıççafalara gösterirken verdik, prodda gider.
        decision = True
        return decision

    def hesapla_satis_ort_sapma(self):
        if self.ort_siparis_tutari_1ay and self.ort_siparis_tutari_12ay:
            return self.x_y_z(self.ort_siparis_tutari_1ay, self.ort_siparis_tutari_12ay)
        else:
            raise ValueError('1 aylık ve(ya) 12 aylık ortalama sipariş tutarlarında kayıt bulunamamıştır !')

    def hesapla_iade_yuzdesi_sapma(self):
        if self.iade_yuzdesi_1 and self.iade_yuzdesi_12:
            return self.x_y_z(self.iade_yuzdesi_1, self.iade_yuzdesi_12)
        else:
            return 0
            # raise ValueError('1 aylık ve(ya) 12 aylık iade yüzdelerinde kayıt bulunamamıştır !')

    @classmethod
    def get_domain_list(cls):
        return [(i.name, i.verbose_name) for i in cls._meta.fields if i not in BaseModel._meta.fields
                and i.verbose_name not in ('basemodel ptr',)]

    def get_field_config_name(self, config_object, **kwargs):
        desired_field = kwargs.get('field')
        if desired_field not in list(self._meta.fields):
            raise ValueError('Specified field is not in Risk Dataset Model')

        excel_field = config_object.get(source_field=desired_field)

        return excel_field

    class Meta:
        db_table = 'RISK_DATA'


class RiskDataSetPoints(BaseModel):
    risk_dataset = models.ForeignKey(DataSetModel, on_delete=models.SET_NULL, db_column='RELATED_RISK',
                                     null=True)
    point = models.FloatField(db_column='CALC_PTS', null=True, blank=True)
    variable = models.CharField(max_length=100, db_column='VARIABLE', null=True, blank=True)

    objects = models.Manager()
    analyzer = AnalyzeManager

    class Meta:
        db_table = 'RISK_DATASET_POINTS'

    def __str__(self):
        return f'POINTS OF {self.risk_dataset}'
