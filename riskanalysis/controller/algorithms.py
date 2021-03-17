import numpy as np
import pandas as pd

from appconfig.models.models import Domains, Subtypes
from riskanalysis.models.managers import BaseAnalyze
from riskanalysis.models.models import DataSetModel, RiskDataSetPoints


class AnalyzingRiskDataSet(BaseAnalyze):
    """
    It also converts bulk data into categorized data
    # todo: 100'den buyukse veya 0'dan kucukse uyari ver.
    """
    analyze_right_now = True

    def __init__(self, riskdataset_pk, analyze_right_now=True):
        super(AnalyzingRiskDataSet, self).__init__(riskdataset_pk)
        self.analyze_right_now = analyze_right_now

    def set_risk_points_object(self, *args, **kwargs):
        r_pts = RiskDataSetPoints(*args, **kwargs)
        r_pts.save()

        risk_dataset = kwargs.get('risk_dataset')
        risk_dataset.risk_pts = r_pts

        return r_pts

    def get_analyzed_data(self):
        return self.analyzed_data

    def analyze_decision_based_on_latest12months_payback(self):
        """
        Son 12 Ay İade %si: İade aylık satışın % 10 unu aşmazsa hesaplama yapılmayacak
        HINT: Puanlaması başka fonksiyonda
        """
        rd = self.get_risk_dataset

        if pd.isna(rd.last_twelve_months_payback_perc):
            print("Son 12 aylık ortalama iade yuzdesi verisi bulunamamıştır. \n"
                  "Analiz kararı (default) Evet olarak verilmiştir.")
            self.analyze_decision = True  # no data but we will analyze

        else:
            if rd.avg_order_amount_last_twelve_months is np.nan:
                print("Analiz karari son 12 aylık ortalama sipariş tutarı verisi olmadığı için verilemedi. \n")
                print("Bu yüzden analiz kararı (default) Evet olarak devam edilecek.")

            else:
                if rd.avg_order_amount_last_twelve_months * 0.1 <= rd.last_twelve_months_payback_perc:
                    self.analyze_decision = False
                    print("Analiz yapilmayacak.")

            return self.analyze_decision

    def detect_son_12ay_satis_ort_sapma(self):
        """
        %0-20 azalış	3
        %20-50 azalış	5
        %50-75 azalış	10
        """

        pnt_df = self.get_intervals_by_name('Son 12 Ay Satış Ortalamasından Sapma', convert_df=True)
        rd = self.get_risk_dataset
        aberration = rd.last_3_months_aberration
        pts = self.get_points_from_value(aberration, pnt_df)

        saved_pts = self.set_risk_points_object(risk_dataset=rd,
                                                variable='Son 12 Ay Satış Ortalamasından Sapma',
                                                calculated_pts=pts)
        return saved_pts

    def analyze_kar(self):
        """
        %0-5	15
        %5-10	10
        %10-15	7
        %15-20	5
        %20 ve üzeri	3

        """
        pnt_df = self.get_intervals_by_name('Kar', convert_df=True)
        rd = self.get_risk_dataset
        profit = rd.profit
        pts = self.get_points_from_value(profit, pnt_df)
        saved_pts = self.set_risk_points_object(risk_dataset=rd, variable='Kar',
                                                calculated_pts=pts)
        return saved_pts

    def analyze_son_12_ay_iade_yuzdesi(self):
        """
        %0-20 	3
        %20-50 	5
        %50-75 	10
        %75 üzeri 	15

        """
        pnt_df = self.get_intervals_by_name('Son 12 ay iade yüzdesi', convert_df=True)
        rd = self.get_risk_dataset
        last_twelve_months_payback_perc = rd.last_twelve_months_payback_perc
        pts = self.get_points_from_value(last_twelve_months_payback_perc, pnt_df)
        saved_pts = self.set_risk_points_object(risk_dataset=rd, variable='Son 12 ay iade yüzdesi',
                                                calculated_pts=pts)
        return saved_pts

    def analyze_ort_gecikme_gun_sayisi(self):
        """
        10 gün	5
        20 gün	10
        30 gün ve üzeri	15

        """
        pnt_df = self.get_intervals_by_name('Ortalama Gecikme Gün Sayısı', convert_df=True)
        rd = self.get_risk_dataset
        avg_delay_time = rd.avg_delay_time
        pts = self.get_points_from_value(avg_delay_time, pnt_df)
        saved_pts = self.set_risk_points_object(variable='Ortalama Gecikme Gün Sayısı',
                                                calculated_pts=pts, risk_dataset=rd)
        return saved_pts

    def analyze_ort_gecikme_gun_bakiyesi(self):
        """
        0-50000	5
        50000-100000	8
        100000 ve üzeri	10

        """
        pnt_df = self.get_intervals_by_name('Ortalama Gecikme Gün Bakiyesi', convert_df=True)
        rd = self.get_risk_dataset
        avg_delay_balance = rd.avg_delay_balance
        pts = self.get_points_from_value(avg_delay_balance, pnt_df)

        saved_pts = self.set_risk_points_object(risk_dataset=rd, calculated_pts=pts,
                                                variable='Ortalama Gecikme Gün Bakiyesi')
        return saved_pts

    def analyze_devir_gunu(self):
        """
        0-15	5
        15-30	10
        30 ve üzeri	15

        """
        pnt_df = self.get_intervals_by_name('Devir Günü', convert_df=True)
        rd = self.get_risk_dataset

        period_day = rd.period_day  # todo bu kısım getter'a verilmeli
        if period_day is None:
            period_day = DataSetManager.hesapla_devir_gunu(rd.period_velocity)

        pts = self.get_points_from_value(period_day, pnt_df)

        saved_pts = self.set_risk_points_object(risk_dataset=rd,
                                                calculated_pts=pts, variable='Devir Günü')
        return saved_pts

    def detect_teminat_limit_riskini_karsilama_seviyesi(self):
        """
        %0-20 	15
        %20-50 	10
        %50-75 	5
        %75 üzeri 	3

        """
        pnt_df = self.get_intervals_by_name('Teminat Limit Riskini Karşılama Seviyesi')
        rd = self.get_risk_dataset
        if (rd.warrant_amount is not None) and (rd.limit is not None):
            teminat_limit_risk_kars_seviyesi = (rd.warrant_amount / rd.limit) * 100
            pts = self.get_points_from_value(teminat_limit_risk_kars_seviyesi, pnt_df)

        else:
            # todo: error and logging ?
            pts = None

        saved_pts = self.set_risk_points_object(variable='Teminat Limit Riskini Karşılama Seviyesi',
                                                risk_dataset=rd, calculated_pts=pts)
        return saved_pts

    def is_it_analyzed(self):
        if RiskDataSetPoints.objects.filter(risk_dataset=self.risk_dataset):
            return True
        else:
            return False

    def compute_general_point(self, overwrite=True):
        pts = RiskDataSetPoints.objects.filter(risk_dataset=self.risk_dataset)
        general_pts = 0

        for p in pts:
            p_cpts = p.calculated_pts
            d_pnt = self.domains.get(name=p.variable).point
            if p_cpts is not None and d_pnt is not None:
                general_pts += p.calculated_pts * self.domains.get(name=p.variable).point

        if overwrite:
            self.get_risk_dataset.analyzed_pts = general_pts
            self.get_risk_dataset.save()

        return general_pts

    def analyze_all(self, again=False):
        if not again:
            if self.is_it_analyzed():
                return True

        # true -> analiz yapilir, false -> yapilmaz. default -> true.
        self.analyze_decision_based_on_latest12months_payback()

        # eger yukaridaki False dondururse hesaplama yapilmaz?<
        if self.analyze_decision:
            self.detect_son_12ay_satis_ort_sapma()
            self.analyze_kar()
            self.analyze_son_12_ay_iade_yuzdesi()
            self.analyze_ort_gecikme_gun_sayisi()
            self.analyze_ort_gecikme_gun_bakiyesi()
            self.analyze_devir_gunu()
            self.detect_teminat_limit_riskini_karsilama_seviyesi()

            return True

        else:
            # todo: logging
            return False
