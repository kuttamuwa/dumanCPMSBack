from django.db import models
from django.db.models import F

from appconfig.controllers.hookers import ImportInternalData
from appconfig.models.models import Domains, Subtypes
from riskanalysis.errors.analyze import *
from riskanalysis.errors.validators import WarrantAmountConflictError, BalanceError, NoImplementedParameter

from checkaccount.models.models import CheckAccount

import pandas as pd
import numpy as np


class BaseAnalyze(models.Manager):
    domains = Domains.objects.all()
    subtypes = Subtypes.objects.all()

    @classmethod
    def check_domain_subtype(cls):
        if not cls.domains or cls.subtypes:
            ImportInternalData.import_all()

        cls.set_domain_subtype()

    @classmethod
    def set_domain_subtype(cls):
        cls.domains = Domains.objects.all()
        cls.subtypes = Subtypes.objects.all()

    def get_intervals_by_name(self, name, convert_df=False):
        d = self.domains.get(name=name)
        s = self.subtypes.filter(domain=d)

        if convert_df:
            s = pd.DataFrame(s.values('max_interval', 'min_interval', 'point'))
            s.fillna(np.inf)

        return s, d.point

    @staticmethod
    def get_domain_sum_points():
        return sum([i['point'] for i in Domains.objects.all().values('point')])

    @staticmethod
    def get_points_from_value(value, dataframe):
        pts = 0

        dataframe['max_interval'].fillna(np.inf, inplace=True)
        dataframe['min_interval'].fillna(np.inf, inplace=True)
        if value is not None:
            for index, row in dataframe.iterrows():
                if row["min_interval"] <= value < row["max_interval"]:
                    try:
                        pts = row['pnt']
                    except KeyError:
                        pts = row['point']

                    return pts
        return pts


class RiskDataSetManager(models.Manager):

    @staticmethod
    def teminat_check(teminat_durumu, teminat_tutari):
        if not teminat_durumu and teminat_tutari:
            raise WarrantAmountConflictError

        if teminat_durumu is None:
            teminat_durumu = False

        return teminat_durumu

    def create(self, *args, **kwargs):
        kwargs['musteri'] = CheckAccount.dummy_creator.check_or_create_dummy(create_dummy=True, *args, **kwargs)
        kwargs['teminat_durumu'] = self.teminat_check(kwargs.get('teminat_durumu'),
                                                      kwargs.get('teminat_tutari'))

        return super(RiskDataSetManager, self).create(*args, **kwargs)
    
    def analyze_check_or_create(self):
        for rd in self.filter(general_point__isnull=True):
            if rd.general_point is None:
                self.analyze_me_and_save(rd=rd)
        
        print("Tüm risk verileri tarandı ve olmayanların analiz puanları güncellendi !")

    @staticmethod
    def __nan_to_none(args, kwargs):
        args = [None if pd.isna(i) else i for i in args]
        kwargs = {k: None if pd.isna(v) else v for k, v in kwargs.items() if k not in ('analyze_now',
                                                                                       'create_account_if_not')}

        return args, kwargs

    def analyze_me_and_save(self, rd):
        general_point, _ = self._analyze(rd, get_subpoints=False)
        return self.update(general_point=general_point)

    def _analyze(self, rd, get_subpoints=True, **kwargs):
        print(f"{rd.musteri.firm_full_name} analiz ediliyor..")

        subpoints = None
        rp = AnalyzeManager(riskdataset=rd)
        general_point = rp.analyze(get_subpoints=get_subpoints)

        return general_point, subpoints

    def check_or_create(self, *args, **kwargs):
        analyze_now = kwargs.get('analyze_now', True)

        args, kwargs = self.__nan_to_none(args, kwargs)

        obj, status = super(RiskDataSetManager, self).get_or_create(*args, **kwargs)

        if analyze_now:
            general_point, pts = self._analyze(obj, **kwargs)
            obj.general_point = general_point
            obj.save()

            return obj, pts

        else:
            return obj, status

    def limit_asimi(self):
        """
        Limit - Bakiye. > 0 -> True else -> False
        :return:
        """
        pklist = []
        for i in self.all():
            if i.limit > i.bakiye:
                pklist.append(i.data_id)

        return self.filter(data_id__in=pklist)

    def _vade_asimi(self):
        """
       vade aşımı ortalaması 0 veya None değil
       :return:
       """
        return self.filter(vade_asimi_ortalamasi__gt=0)

    def _iade_self_artis(self):
        """
        İadesi geçmiş aylara kıyasla artarsa?
        iade_12 < iade_1 ise alalım
        :return:
        """
        # todo: iyice deneyelim
        # return self.filter(iade_yuzdesi_1__gt=F('iade_yuzdesi_12'))

        pklist = []
        for i in self.all():
            i_1 = i.iade_yuzdesi_1
            i_12 = i.iade_yuzdesi_12
            if i_1 is not None and i_12 is not None:
                if i_1 > i_12:
                    pklist.append(i.data_id)

        return self.filter(data_id__in=pklist)

    def _sektor_kara_liste(self):
        """
        Sektör kara listede olanlar
        :return:
        """
        raise NotImplementedError

    def _sgk_borcu_olanlar(self):
        """
        SGK Borcu olanlar
        :return:
        """
        raise NotImplementedError()

    def _iade_baskalariyla_artis(self):
        """
        İadesi başka müşterilere kıyasla artmış?
        Son 1 ay diye kabul edelim
        iade_1 > avg(iade_1 for other customers)
        :return:
        """
        iade_1_ort = self.exclude(iade_yuzdesi_1__isnull=True)
        if len(iade_1_ort) > 0:
            iade_1_ort = [i for i in self.values('iade_yuzdesi_1') if i is not None]
            iade_1_ort = sum(iade_1_ort) // len(iade_1_ort)

            iade_1_ort = self.filter(iade_yuzdesi_1__gte=iade_1_ort)

        return iade_1_ort

    def _devir_hizi_self_artmis(self):
        """
        Alacak devir hızı geçmiş aylara kıyasla artarsa
        :return:
        """
        pklist = []

        for i in self.all():
            try:
                d_hizi_1 = i.hesapla_devir_hizi(ay=1)
                d_hizi_12 = i.hesapla_devir_hizi(ay=12)

                if d_hizi_12 > d_hizi_1:
                    pklist.append(i.data_id)

            except BalanceError:
                pass

        return self.filter(data_id__in=pklist)

    def _ort_devir_hizi(self, ay=1):
        """
        Ortalama devir hizi. ay = 1
        :return:
        """
        if ay == 1:
            values = [i.hesapla_devir_hizi() for i in self.all()]
        elif ay == 12:
            values = [i.hesapla_devir_hizi(ay=12) for i in self.all()]

        else:
            raise NoImplementedParameter

        return sum(values) // len(values)

    def _devir_hizi_baskalariyla_artmis(self):
        """
        Alacak devir hızı genel müşteri ortalamasına kıyasla yüksekse
        Son 1 ay alalim
        :return:
        """
        devir_hizi_ort_1ay = self._ort_devir_hizi(ay=1)
        pklist = [i.data_id for i in self.all() if i.hesapla_devir_hizi() < devir_hizi_ort_1ay]

        return pklist

    def asim_yapanlar(self, dtype):
        """
        :return:
        """
        print("Vade asimi yapanlar bulunur")
        dtype_list = {'v': self._vade_asimi,
                      'dhself': self._devir_hizi_self_artmis,
                      'dhothers': self._devir_hizi_baskalariyla_artmis,
                      'l': self.limit_asimi,
                      'i1': self._iade_self_artis,
                      'i2': self._iade_baskalariyla_artis,
                      's': self._sgk_borcu_olanlar,
                      'skl': self._sektor_kara_liste}
        fnc = dtype_list[dtype]
        try:
            pklist = fnc()
            return self.filter(pk__in=pklist)
        except NotImplementedError:
            print("No implemented error")


class AnalyzeManager(BaseAnalyze):
    _riskdataset = None

    def __init__(self, riskdataset):
        self._riskdataset = riskdataset

    @property
    def riskdataset(self):
        return self._riskdataset

    @riskdataset.setter
    def riskdataset(self, value):
        self.riskdataset = value

    def kontrol(self):
        if self.riskdataset is None:
            raise NoRiskDataset
        self.check_domain_subtype()

    @staticmethod
    def calc_general_point(**pts):
        domain_sum_pts = pts['domain_sum_pts']
        sum_pts = sum([v for _, v in pts.items() if _ != 'domain_sum_pts'])
        general_point = sum_pts / domain_sum_pts

        return general_point

    def analyze(self, get_subpoints=False):
        self.kontrol()
        analiz_karari = self.analiz_karari()

        # todo: en son kaldır
        analiz_karari = True

        if analiz_karari:
            pts = self.calc_all_pts()
            general_point = self.calc_general_point(**pts)
            if get_subpoints:
                return general_point, pts
            else:
                return general_point

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
        pts = pts * domain_point

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
        pts = pts * domain_point

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
        pts = pts * domain_point

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
        pts = pts * domain_point

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
        pts = pts * domain_point

        return pts

    def karsilastirma_teminat_limit(self):
        """
        %0-20 	15
        %20-50 	10
        %50-75 	5
        %75 üzeri 	3

        """
        pnt_df, domain_point = self.get_intervals_by_name('Teminat Limiti', convert_df=True)
        teminat_limit_risk_kars_seviyesi = self.riskdataset.hesapla_karsilastir_teminat_limit()
        pts = self.get_points_from_value(teminat_limit_risk_kars_seviyesi, pnt_df)
        pts = pts * domain_point

        return pts

    def calc_all_pts(self):
        pts_satis_ort = self.karsilastirma_son_12ay_satis_ort()
        pts_iade_yuzdesi = self.karsilastirma_son_12_ay_iade_yuzdesi()
        pts_gecikme_bakiye = self.ort_gecikme_gun_bakiyesi()
        pts_gecikme_sayisi = self.ort_gecikme_gun_sayisi()
        pts_devir_gunu = self.devir_gunu()
        pts_teminat_riski = self.karsilastirma_teminat_limit()

        return {
            'Son 12 Ay Satış Ortalamasından Sapma': pts_satis_ort,
            'Son 12 ay iade yüzdesi': pts_iade_yuzdesi,
            'Ortalama Gecikme Gün Bakiyesi': pts_gecikme_bakiye,
            'Ortalama Gecikme Gün Sayısı': pts_gecikme_sayisi,
            'Devir Günü': pts_devir_gunu,
            'Teminat Limiti': pts_teminat_riski,
            'domain_sum_pts': self.get_domain_sum_points()
        }

        # sum_pts = sum([pts_satis_ort, pts_iade_yuzdesi, pts_gecikme_bakiye, pts_gecikme_sayisi,
        #                pts_devir_gunu, pts_teminat_riski])
        # domain_sum_pts = self.get_domain_sum_points()
        # general_point = sum_pts / domain_sum_pts

        # return general_point


class RiskDatasetPointsManager(models.Manager):
    pass


class BaseDummyCreator(models.Manager):
    def gen_user(self, musteri, *args, **kwargs):
        kwargs = self.gen_aburcubur_attrs(**kwargs)

        obj = self.create(musteri=musteri)
        print(f"Sanal risk verisi üretildi : {obj.firm_full_name}")
        return obj


class DummyRiskAnalysisCreator(BaseDummyCreator):
    def check_or_create_dummy(self, musteri, *args, **kwargs):
        try:
            return self.get(musteri=musteri)
        except models.ObjectDoesNotExist:
            return self.gen_user(musteri, *args, **kwargs)
