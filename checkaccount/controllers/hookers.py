import os

import pandas as pd

from checkaccount.models.models import Cities, Districts, SysPersonnel, SysDepartments, CheckAccount, Sectors
from dumanCPMSRevise.settings import DEBUG, BASE_DIR


class BaseImport:
    folder_path = os.path.join(BASE_DIR, 'checkaccount', 'data')
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


class ImportCityDistrict(BaseImport):
    data = 'ILCELER.xlsx'

    @staticmethod
    def _save(df):
        for index, row in df.iterrows():
            c = Cities.objects.get_or_create(name=row.ILADI, city_plate_number=row.ILKODU)[0]
            Districts.objects.get_or_create(city=c, name=row.ILCEADI, ilcekodu=row.ILCEKODU)

        print("İl ve ilçeler yüklendi")
        return True

    @staticmethod
    def delete_districts():
        Districts.objects.all().delete()

    @staticmethod
    def delete_cities():
        Cities.objects.all().delete()

    def runforme(self):
        if not DEBUG:
            df = self.read_from_excel()
            self._save(df)


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

    def runforme(self):
        if not DEBUG:
            df = self.read_from_excel()
            self._save(df)


class ImportAccounts(BaseImport):
    data = 'accounts.xlsx'

    @staticmethod
    def create_dummy_accounts(df):
        for _, row in df.iterrows():
            CheckAccount.dummy_creator.get_or_create(**dict(row))
        print("Dummy veriler yüklendi")

    def runforme(self):
        if not DEBUG:
            df = self.read_from_excel()

            self.create_dummy_accounts(df)


class ImportSectors(BaseImport):
    data = 'sektorler.xlsx'

    @staticmethod
    def _save(df):
        for index, row in df.iterrows():
            sektor = row.SEKTORADI
            Sectors.objects.get_or_create(name=sektor)

    def runforme(self):
        if not DEBUG:
            df = self.read_from_excel()
            self._save(df)

            print("Sektörler yüklendi")
