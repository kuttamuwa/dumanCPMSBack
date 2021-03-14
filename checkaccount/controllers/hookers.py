import os

import pandas as pd

from checkaccount.models.models import Cities, Districts, SysPersonnel, SysDepartments, CheckAccount


class BaseImport:
    folder_path = os.path.abspath('./checkaccount/data')
    data = None

    def read_from_excel(self):
        data_excel = os.path.join(self.folder_path, self.data)
        df = pd.read_excel(data_excel)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        return df

    @staticmethod
    def _save(df):
        raise NotImplementedError

    def test_runforme(self):
        raise NotImplementedError


class ImportCityDistrict(BaseImport):
    data = 'ilceler.xlsx'

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


class ImportPersonnels(BaseImport):
    data = 'personnels.xlsx'

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


class ImportAccounts(BaseImport):
    data = 'accounts.xlsx'

    @staticmethod
    def _save(df):
        for index, row in df.iterrows():
            CheckAccount.objects.get_or_create(**row)

    def test_runforme(self):
        if len(CheckAccount.objects.all()) == 0:
            df = self.read_from_excel()
            self._save(df)

            print("Imported test check accounts")
