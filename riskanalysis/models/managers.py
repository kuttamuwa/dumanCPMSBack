from django.db import models

from appconfig.models.models import Domains, Subtypes
from riskanalysis.errors.analyze import *
from riskanalysis.errors.validators import WarrantAmountConflictError

"""
:exception: Şu anda Customer sütunu CheckAccount üzerinden gelmektedir. 
Check Account modülü satılmayacaksa aşağıdan DummyUser olarak gösterilmesi gerekir

"""
try:
    from checkaccount.models.models import CheckAccount

except ImportError:
    from riskanalysis.adaptors.user import DummyUser as CheckAccount

import pandas as pd
import numpy as np


class BaseAnalyze(models.Manager):
    domains = Domains.objects.all()
    subtypes = Subtypes.objects.all()

    def get_intervals_by_name(self, name, convert_df=False):
        d = self.domains.get(name=name)
        s = self.subtypes.filter(domain=d)

        if convert_df:
            df = pd.DataFrame(s.values('max_interval', 'min_interval', 'point'))
            return df

        return s, d.point

    @staticmethod
    def get_points_from_value(value, dataframe):
        pts = None

        if value is not None:
            for index, row in dataframe.iterrows():
                if row["min_interval"] < value < row["max_interval"]:
                    try:
                        pts = row['pnt']
                    except KeyError:
                        pts = row['point']

        return pts


class RiskDataSetManager(models.Manager):
    def user_check(self, musteri, create_dummy=True):
        if musteri is None:
            if create_dummy:
                return CheckAccount.dummy_creator.create_dummy()
            else:
                raise CheckAccount.DoesNotExist

    def teminat_check(self, teminat_durumu, teminat_tutari):
        if not teminat_durumu and teminat_tutari:
            raise WarrantAmountConflictError

    def create(self, *args, **kwargs):
        kwargs['musteri'] = self.user_check(musteri=kwargs.get('musteri'))
        self.teminat_check(kwargs.get('teminat_durumu'), kwargs.get('teminat_tutari'))

        return super(RiskDataSetManager, self).create(*args, **kwargs)


class AnalyzeManager(models.Manager):
    _riskdataset = None

    @property
    def riskdataset(self):
        return self._riskdataset

    @riskdataset.setter
    def riskdataset(self, value):
        self.riskdataset = value

    def kontrol(self):
        if self.riskdataset is None:
            raise NoRiskDataset

    def analyze(self):
        self.kontrol()

    def analiz_karari(self):
        """
        Son 12 Ay İade %si: İade aylık satışın % 10 unu aşmazsa hesaplama yapılmayacak
        HINT: Puanlaması başka fonksiyonda
        """

        analiz_karari = self.riskdataset.hesapla_analiz_karari()
        return analiz_karari

    def karsilastirma_son_12ay_satis_ort(self):
        """
        %0-20 azalış	3
        %20-50 azalış	5
        %50-75 azalış	10
        """

        pnt_df, domain_point = self.get_intervals_by_name('Son 12 Ay Satış Ortalamasından Sapma', convert_df=True)
        siparis_ort_sapma = self.riskdataset.hesapla_satis_ort_sapma()

        pts = self.get_points_from_value(siparis_ort_sapma, pnt_df)

        # multiply by domain point

        return pts

    def karsilastirma_son_12_ay_iade_yuzdesi(self):
        """
        %0-20 	3
        %20-50 	5
        %50-75 	10
        %75 üzeri 	15

        """
        pnt_df, domain_point = self.get_intervals_by_name('Son 12 ay iade yüzdesi', convert_df=True)
        iade_yuzdesi_sapma = self.riskdataset.hesapla_iade_yuzdesi_sapma()
        pts = self.get_points_from_value(iade_yuzdesi_sapma, pnt_df)

        return pts

    def ort_gecikme_gun_sayisi(self):
        """
        10 gün	5
        20 gün	10
        30 gün ve üzeri	15

        """
        pnt_df, domain_point = self.get_intervals_by_name('Ortalama Gecikme Gün Sayısı', convert_df=True)
        ort_gecikme_gun_sayisi = self.riskdataset.ort_gecikme_gun_sayisi
        pts = self.get_points_from_value(ort_gecikme_gun_sayisi, pnt_df)

        return pts

    def ort_gecikme_gun_bakiyesi(self):
        """
        0-50000	5
        50000-100000	8
        100000 ve üzeri	10

        """
        pnt_df, domain_point = self.get_intervals_by_name('Ortalama Gecikme Gün Bakiyesi', convert_df=True)
        ort_gecikme_gun_bakiyesi = self.riskdataset.ort_gecikme_gun_bakiyesi
        pts = self.get_points_from_value(ort_gecikme_gun_bakiyesi, pnt_df)

        return pts

    def devir_gunu(self):
        """
        0-15	5
        15-30	10
        30 ve üzeri	15

        """
        pnt_df, domain_point = self.get_intervals_by_name('Devir Günü', convert_df=True)
        devir_gunu = self.riskdataset.hesapla_devir_gunu()
        pts = self.get_points_from_value(devir_gunu, pnt_df)

        return pts

    def karsilastirma_teminat_limit(self):
        """
        %0-20 	15
        %20-50 	10
        %50-75 	5
        %75 üzeri 	3

        """
        pnt_df, domain_point = self.get_intervals_by_name('Devir Günü', convert_df=True)
        teminat_limit_risk_kars_seviyesi = self.riskdataset.hesapla_karsilastir_teminat_limit()
        pts = self.get_points_from_value(teminat_limit_risk_kars_seviyesi, pnt_df)

        return pts

    def calc_all_pts(self):
        pts_satis_ort = self.karsilastirma_son_12ay_satis_ort()
        pts_iade_yuzdesi = self.karsilastirma_son_12_ay_iade_yuzdesi()
        pts_gecikme_bakiye = self.ort_gecikme_gun_bakiyesi()
        pts_gecikme_sayisi = self.ort_gecikme_gun_sayisi()
        pts_devir_gunu = self.devir_gunu()
        pts_teminat_riski = self.karsilastirma_teminat_limit()

    def create(self, *args, **kwargs):
        rd = self.objects.get(pk=kwargs.get('riskdataset_pk'))
        self.riskdataset = rd

        analiz_karari = self.analiz_karari()

        return super(AnalyzeManager, self).create(*args, **kwargs)