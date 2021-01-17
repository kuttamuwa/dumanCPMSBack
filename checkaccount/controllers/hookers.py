import pandas as pd
import os

from checkaccount.models.models import Cities, Districts


class ImportCityDistrict:
    folder_path = r"C:\Users\LENOVO\PycharmProjects\dumanCPMSRevise\checkaccount\tests"
    iller = 'iller.xlsx'
    ilceler = 'ilceler.xlsx'

    def read_from_excel(self):
        ilce_excel = os.path.join(self.folder_path, self.ilceler)
        df = pd.read_excel(ilce_excel)

        return df

    @staticmethod
    def _save(df):
        for index, row in df.iterrows():
            il = row['adm1_en']
            ilce = row['adm2_en']
            c = Cities.objects.get_or_create(name=il)[0]
            Districts.objects.get_or_create(city=c, name=ilce)

        return True

    def test_runforme(self):
        if len(Districts.objects.all()) == 0:
            df = self.read_from_excel()
            self._save(df)

            print("Imported city and districts")