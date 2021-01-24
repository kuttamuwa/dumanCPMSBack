import pandas as pd
import os

from appconfig.models.models import VergiBorcuListesi, SGKBorcuListesi


class ImportExternalData:
    folder_path = r"C:\Users\LENOVO\PycharmProjects\DumanCPMS\docs\externaldata"
    vergiborcu = "vergi_yuzsuz.xlsx"
    sgkborcu = "sgklar.xlsx"
    sektorkaraliste = "il_ilce_sektor.xlsx"
    konkordataliste = ""

    def vergi_yukle(self):
        df = self.read_from_excel(self.vergiborcu)
        for index, row in df.iterrows():
            daire = row.get('Vergi Dairesi')
            kno = row.get('Vergi Kimlik No')
            adsoyad = row.get('Adı Soyadı')
            faaliyet_konusu = row.get('Esas Faaliyet Konusu')
            borcu = row.get('Vergi Borcu')
            VergiBorcuListesi.objects.get_or_create(vergi_departmani=daire,
                                                    kimlikno=kno,
                                                    borc_sahibi=adsoyad,
                                                    esas_faaliyet_konusu=faaliyet_konusu,
                                                    borc_miktari=borcu)

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
        raise NotImplementedError
