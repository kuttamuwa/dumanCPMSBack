import os

import pandas as pd
from numpy import nan

from checkaccount.models.models import CheckAccount
from dumanCPMSRevise.settings import BASE_DIR
from riskanalysis.models.models import DataSetModel, RiskDataSetPoints
from riskanalysis.views.api import AnalyzeBaseError


class BaseImport:
    folder_path = os.path.join(BASE_DIR, 'riskanalysis', 'data')
    data = None

    def read_from_excel(self):
        data_excel = os.path.join(self.folder_path, self.data)
        df = pd.read_excel(data_excel)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        return df

    @staticmethod
    def _save(df):
        raise NotImplementedError

    def runforme(self):
        raise NotImplementedError


class ImportRiskDataset(BaseImport):
    personnels = 'OrnekMPYSTurkcev2.xlsx'

    def read_from_excel(self):
        personel_df = os.path.join(self.folder_path, self.personnels)
        df = pd.read_excel(personel_df)

        return df

    @staticmethod
    def _save(df):
        df.replace(nan, None, inplace=True)
        for index, row in df.iterrows():
            # adsoyad = row.get('Müşteri')
            taxpayer_number = int(row.get('VKNTC'))

            row = row.drop(['VKNTC'], axis=0)

            musteri = CheckAccount.dummy_creator.check_or_create_dummy(taxpayer_number=taxpayer_number)
            limit = row.get('Limit')

            # teminat = row.get(
            teminat_durumu = row.get('Teminat Durumu')
            teminat_tutari = row.get('Teminat Tutarı')

            # vade ve odeme = row.get(
            vade = row.get('Vade')
            vade_asimi_ortalamasi = row.get('Ort. Vade Aşımı')
            odeme_sikligi = row.get('Ödeme Sıklığı')

            # Sipariş tutarlar
            ort_siparis_tutari_12ay = row.get('Son 12 Ay Ortalama Sipariş Tutarı')
            ort_siparis_tutari_1ay = row.get('Son 1 Ay Ortalama Sipariş Tutarı')

            # iade yüzdeleri
            iade_yuzdesi_1 = row.get('Son 1 ay iade yüzdesi', None)
            iade_yuzdesi_12 = row.get('Son 12 ay iade yüzdesi')

            # gecikmeler
            ort_gecikme_gun_sayisi = row.get('Ort. Gecikme Gün Sayısı')
            ort_gecikme_gun_bakiyesi = row.get('Ort. Gecikme Gün Bakiyesi (TL)')

            # simdi mi analiz edilsin?
            analyze_now = row.get('Analiz Et', True)

            bakiye = row.get('Bakiye')
            obj, pts = DataSetModel.objects.check_or_create(musteri=musteri, limit=limit, teminat_durumu=teminat_durumu,
                                                            teminat_tutari=teminat_tutari,
                                                            vade=vade, vade_asimi_ortalamasi=vade_asimi_ortalamasi,
                                                            odeme_sikligi=odeme_sikligi,
                                                            ort_siparis_tutari_1ay=ort_siparis_tutari_1ay,
                                                            ort_siparis_tutari_12ay=ort_siparis_tutari_12ay,
                                                            iade_yuzdesi_1=iade_yuzdesi_1,
                                                            iade_yuzdesi_12=iade_yuzdesi_12,
                                                            ort_gecikme_gun_sayisi=ort_gecikme_gun_sayisi,
                                                            ort_gecikme_gun_bakiyesi=ort_gecikme_gun_bakiyesi,
                                                            bakiye=bakiye,
                                                            analyze_now=analyze_now)
        return True

    def runforme(self):
        print("Risk dataseti yukleyelim")
        df = self.read_from_excel()
        self._save(df)

        print("Imported risk datasets")


class AnalyzeRiskDataset:
    @classmethod
    def analyze_all(cls):
        try:
            DataSetModel.objects.analyze_check_or_create()
            print("Risk Dataset verilerinin tamamı tarandı ve analiz puanları güncellendi ")

        except Exception as err:
            err = f'{AnalyzeBaseError.default_detail} \n Kaynak Hata : {err}'
            print(f"Lan hata aldık ! : {err}")
            raise AnalyzeBaseError(default_detail=err)
