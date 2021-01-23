import pandas as pd
import os

from checkaccount.models.models import Cities, Districts, SysPersonnel, SysDepartments


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


class ImportPersonnels:
    folder_path = r"C:\Users\LENOVO\PycharmProjects\dumanCPMSRevise\checkaccount\tests"
    personnels = 'personnels.xlsx'

    def read_from_excel(self):
        personel_df = os.path.join(self.folder_path, self.personnels)
        df = pd.read_excel(personel_df)

        return df

    @staticmethod
    def _save(df):
        for index, row in df.iterrows():
            firstname = row['firstname']
            surname = row['surname']
            username = row['username']
            department = SysDepartments.objects.get_or_create(department_name=row['department'])[0]
            position = row['position']

            SysPersonnel.objects.get_or_create(firstname=firstname, surname=surname, username=username,
                                               department=department, position=position)

        return True

    def test_runforme(self):
        if len(SysPersonnel.objects.all()) == 0:
            df = self.read_from_excel()
            self._save(df)

            print("Imported sys personnels")
