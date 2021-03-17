import pandas as pd
import os

from appconfig.models.models import VergiBorcuListesi, SGKBorcuListesi
from dumanCPMSRevise.settings import BASE_DIR


class ImportExternalData:
    folder_path = os.path.join(BASE_DIR, 'appconfig', 'data', 'externaldata')
    vergiborcu = "vergi_yuzsuz.xlsx"
    sgkborcu = "sgklar.xlsx"
    sektorkaraliste = "il_ilce_sektor.xlsx"
    konkordataliste = ""

    def vergi_yukle(self):
        from checkaccount.models.models import CheckAccount

        df = self.read_from_excel(self.vergiborcu)
        kno_list = tuple(df['Vergi Kimlik No'])
        # related_accounts = CheckAccount.objects.filter(taxpayer_number__in=kno_list).values_list('taxpayer_number')
        df = df[df['Vergi Kimlik No'].isin(kno_list)]

        for index, row in df.iterrows():
            daire = row.get('Vergi Dairesi')
            kno = row.get('Vergi Kimlik No')
            adsoyad = row.get('Adı Soyadı')
            faaliyet_konusu = row.get('Esas Faaliyet Konusu')
            borcu = row.get('Vergi Borcu')

            try:
                acc = CheckAccount.objects.get(taxpayer_number=kno)
                VergiBorcuListesi.objects.get_or_create(vergi_departmani=daire,
                                                        borc_sahibi=acc,
                                                        esas_faaliyet_konusu=faaliyet_konusu,
                                                        borc_miktari=borcu)
            except CheckAccount.DoesNotExist:
                # iliskili kayit yok, pas gecilir.
                pass

        return True

    def sgk_yukle(self):
        df = self.read_from_excel(self.sgkborcu)
        for index, row in df.iterrows():
            kimlikno = row.get('Kimlik No')
            adsoyad = row.get('Ad Soyad')
            borcu = row.get('Borç Tutarı')

            SGKBorcuListesi.objects.get_or_create(
                kimlikno=kimlikno,
                borc_sahibi=adsoyad,
                borc_miktari=borcu
            )

    def sektorkaraliste_yukle(self):
        raise NotImplementedError
        # df = self.read_from_excel(self.sektorkaraliste)

    def konkordato_yukle(self):
        raise NotImplementedError

    def read_from_excel(self, filename):
        file_excel = os.path.join(self.folder_path, filename)
        df = pd.read_excel(file_excel)

        return df

    @staticmethod
    def _save(df):
        raise NotImplementedError

    def runforme(self):
        # pass
        self.vergi_yukle()
        self.sgk_yukle()

