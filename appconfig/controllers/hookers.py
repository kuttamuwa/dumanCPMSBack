import os

import pandas as pd

from appconfig.models.models import VergiBorcuListesi, SGKBorcuListesi, Domains, Subtypes
from checkaccount.models.models import CheckAccount
from dumanCPMSRevise.settings import BASE_DIR, DEBUG


# from riskanalysis.models.models import DataSetModel


class BaseImport:
    folder_path = os.path.join(BASE_DIR, 'appconfig', 'data')
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


class ImportDomainData(BaseImport):
    @staticmethod
    def _save(df):
        print("Excelden domainleri yukleyelim")

        for index, row in df.iterrows():
            name = row['name']
            point = row['point']

            d = Domains(name=name, point=point)
            d.save()

        print("Domainler yüklendi")

    data = 'Domains.xlsx'

    def runforme(self):
        if not DEBUG:
            if len(Domains.objects.all()) == 0:
                df = self.read_from_excel()
                self._save(df)


class ImportSubtypeData(BaseImport):
    @staticmethod
    def _save(df):
        print("Subtypelari excelden yukleyelim")

        for index, row in df.iterrows():
            domain_name = row['domain_name']
            d = Domains.objects.get(name=domain_name)
            point = row['point']
            min_interval = row['min_interval']
            max_interval = row['max_interval']

            s = Subtypes(domain=d, min_interval=min_interval, max_interval=max_interval,
                         point=point)
            s.save()
        print("Subtypelar yüklendi")

    data = 'Subtypes.xlsx'

    def runforme(self):
        if not DEBUG:
            if len(Subtypes.objects.all()) == 0:
                df = self.read_from_excel()
                self._save(df)


class ImportInternalData:
    @classmethod
    def import_all(cls):
        ImportDomainData().runforme()
        ImportSubtypeData().runforme()


class ImportExternalData:
    folder_path = os.path.join(BASE_DIR, 'appconfig', 'data', 'externaldata')
    vergiborcu = "vergi_yuzsuz.xlsx"
    sgkborcu = "sgklar.xlsx"
    sektorkaraliste = "il_ilce_sektor.xlsx"
    konkordataliste = ""

    def ca_check(self):
        # check account data yuklendi mi
        from checkaccount.controllers.apps import CheckaccountConfig
        CheckaccountConfig.import_account_data()

    def vergi_yukle(self):
        print("Vergi borçlularını yükleyelim")
        from checkaccount.models.models import CheckAccount

        df = self.read_from_excel(self.vergiborcu)
        kno_list = tuple(df['Vergi Kimlik No'])

        df = df[df['Vergi Kimlik No'].isin(kno_list)]

        for index, row in df.iterrows():
            daire = row.get('Vergi Dairesi')
            kno = row.get('Vergi Kimlik No')
            adsoyad = row.get('Adı Soyadı')
            faaliyet_konusu = row.get('Esas Faaliyet Konusu')
            borcu = row.get('Vergi Borcu')

            try:
                acc = CheckAccount.objects.get(
                    firm_full_name=adsoyad,
                    taxpayer_number=kno
                )
                VergiBorcuListesi.objects.check_or_create(vergi_departmani=daire,
                                                          borc_sahibi=acc,
                                                          esas_faaliyet_konusu=faaliyet_konusu,
                                                          borc_miktari=borcu)

            except CheckAccount.DoesNotExist:
                pass

            except Exception as err:
                print(f"Vergi borçluları yüklenirken hata : {str(err)}")

        print("Vergi borçluları tarama yükleme tamamlandı")

    def sgk_yukle(self):
        print("SGK borçlularını yükleyelim")
        df = self.read_from_excel(self.sgkborcu)

        # sadece kimlik no uyusanlar
        df = df[df['Kimlik No'].isin([int(i['taxpayer_number'])
                                      for i in CheckAccount.objects.values('taxpayer_number')])]

        for index, row in df.iterrows():
            kimlikno = row.get('Kimlik No')
            adsoyad = row.get('Ad Soyad')
            borcu = row.get('Borç Tutarı')

            try:
                borc_sahibi = CheckAccount.objects.get(
                    firm_full_name=adsoyad,
                    taxpayer_number=kimlikno,
                )
                SGKBorcuListesi.objects.get_or_create(
                    kimlikno=kimlikno,
                    borc_sahibi=borc_sahibi,
                    borc_miktari=borcu
                )

            except CheckAccount.DoesNotExist:
                pass

            except Exception as err:
                print(f"SGK yüklenirken hata : {str(err)}")

        print("SGK borçluları tarama yükleme tamamlandı")

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
        if not DEBUG:
            self.ca_check()
            self.vergi_yukle()
            self.sgk_yukle()

            print("Cari hesaplar yüklendi. Bunlarla ilişkili vergi borçluları ve SGK borçluları varsa sisteme yüklendi "
                  "ve eşleştirildi.")