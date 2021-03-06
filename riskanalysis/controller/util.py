import pandas as pd


class RiskAnalysisUtil:
    def __init__(self):
        pass

    def import_from_excel(self, path):
        df = pd.read_excel(path)

        # Analyzing process
        model_lists = []
        for index, row in df.iterrows():
            musteri = self.nan_to_none(row.get('Müşteri'))
            limit = self.nan_to_none(row.get('Limit'))

            # teminat
            teminat_durumu = self.nan_to_none(row.get('Teminat Durumu'))
            teminat_tutari = self.nan_to_none(row.get('Teminat Tutarı'))

            # vade ve odeme
            vade = self.nan_to_none(row.get('Vade'))
            vade_asimi_ortalamasi = self.nan_to_none(row.get('Ort. Gecikme Gün Bakiyesi (TL)'))
            odeme_sikligi = self.nan_to_none(row.get('Ödeme Sıklığı'))

            # Sipariş tutarları
            ort_siparis_tutari_12ay = self.nan_to_none(row.get('Son 12 Ay Ortalama Sipariş Tutarı'))
            ort_siparis_tutari_1ay = self.nan_to_none(row.get('Son 1 Ay Ortalama Sipariş Tutarı'))

            # iade yüzdeleri
            iade_yuzdesi_1 = self.nan_to_none(row.get('Son 1 ay iade yüzdesi'))
            iade_yuzdesi_12 = self.nan_to_none(row.get('Son 12 ay iade yüzdesi'))

            # gecikmeler
            ort_gecikme_gun_sayisi = self.nan_to_none(row.get('Ort. Gecikme Gün Sayısı'))
            ort_gecikme_gun_bakiyesi = self.nan_to_none(row.get('Ort. Gecikme Gün Bakiyesi (TL)'))

            bakiye = self.nan_to_none(row.get('Bakiye'))

            model_dict = {
                "musteri": musteri, "limit": limit, "teminat_durumu": teminat_durumu,
                "teminat_tutari": teminat_tutari, "vade": vade, "vade_asimi_ortalamasi": vade_asimi_ortalamasi,
                "odeme_sikligi": odeme_sikligi, "ort_siparis_tutari_12ay": ort_siparis_tutari_12ay,
                "ort_siparis_tutari_1ay": ort_siparis_tutari_1ay,
                "iade_yuzdesi_1": iade_yuzdesi_1, "iade_yuzdesi_12": iade_yuzdesi_12,
                "ort_gecikme_gun_sayisi": ort_gecikme_gun_sayisi, "ort_gecikme_gun_bakiyesi": ort_gecikme_gun_bakiyesi,
                "bakiye": bakiye}
            model_lists.append(model_dict)

        return model_lists

    @staticmethod
    def nan_to_none(value):
        if pd.isna(value):
            value = None

        return value
