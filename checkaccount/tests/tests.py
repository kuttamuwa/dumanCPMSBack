import os
from abc import ABC

import pandas as pd

from django.test import TestCase

from checkaccount.controllers.hookers import ImportCityDistrict
from checkaccount.models.models import SysDepartments, SysPersonnel, Cities, Districts, CheckAccount, Sectors


class CityDistrictsTest(TestCase):
    @staticmethod
    def test_runforme():
        ImportCityDistrict().test_runforme()


class SysDepartmentsTest(TestCase):
    @staticmethod
    def test_create_test_departments():
        SysDepartments.objects.get_or_create(department_name='FINANCE')
        SysDepartments.objects.get_or_create(department_name='HR')
        SysDepartments.objects.get_or_create(department_name='IT')
        SysDepartments.objects.get_or_create(department_name='GIS')
        SysDepartments.objects.get_or_create(department_name='MIS')

    @staticmethod
    def test_get_all_departments():
        print("all departments : \n")
        departments = SysDepartments.objects.all()
        print(departments)
        return departments


class SysPersonnelTest(TestCase):
    @staticmethod
    def test_create_personels():
        SysDepartmentsTest.test_create_test_departments()

        SysPersonnel.objects.get_or_create(firstname='mert', surname='öner', username='moner',
                                           department=SysDepartments.objects.get(department_name='FINANCE'),
                                           position='MARKETING')
        SysPersonnel.objects.get_or_create(firstname='umut', surname='ucok', username='uucok',
                                           department=SysDepartments.objects.get(department_name='MIS'),
                                           position='ENGINEER')
        SysPersonnel.objects.get_or_create(firstname='mustafa', surname='duman', username='mduman',
                                           department=SysDepartments.objects.get(department_name='IT'),
                                           position='CEO')
        SysPersonnel.objects.get_or_create(firstname='salim', surname='onurbilen', username='sonurbilen',
                                           department=SysDepartments.objects.get(department_name='GIS'),
                                           position='ENGINEER')
        SysPersonnel.objects.get_or_create(firstname='enes', surname='duman', username='eduman',
                                           department=SysDepartments.objects.get(department_name='IT'),
                                           position='CTO')
        print("many users were created !")


class SectorTest(TestCase):
    @staticmethod
    def test_create_sectors():
        Sectors.objects.get_or_create(name='FINANCE')
        Sectors.objects.get_or_create(name='GIS')
        Sectors.objects.get_or_create(name='IT')
        Sectors.objects.get_or_create(name='IOT')
        Sectors.objects.get_or_create(name='GAME DEVELOPMENT')
        Sectors.objects.get_or_create(name='AKILLI EV')

        print("Many sectors are created")


class CheckAccountTest(TestCase):
    excel_path = r"C:\Users\LENOVO\PycharmProjects\DumanCPMS\excels\CheckAccountsTest.xls"

    @staticmethod
    def test_create_one_account():
        # required tables and data
        SysPersonnelTest.test_create_personels()
        SectorTest.test_create_sectors()
        cd = CityDistrictsTest()
        cd.test_runforme()

        s = Sectors.objects.get(name='GIS')
        sp = SysPersonnel.objects.get(username='sonurbilen')
        c = Cities.objects.get(name='CORUM')
        d = Districts.objects.get(name='ISKILIP', city=c)

        c = CheckAccount.objects.get_or_create(firm_type='SAHIS_ISLETMESI', firm_full_name='UMUT TEST AS',
                                               taxpayer_number=18319776776,
                                               tax_department='UMRANIYE VERGI DAIRESI',
                                               firm_address='sample address',
                                               firm_key_contact_personnel=sp,
                                               city=c,
                                               district=d,
                                               sector=s,
                                               phone_number='05063791026',
                                               fax='02122451517', web_url='https://dumanarge.com',
                                               email_addr='info@dumanarge.com')

        c = c[0]
        return c

    @staticmethod
    def test_create_one_account_api():
        # we will send post request to api
        api_url = "http://127.0.0.1:8000/checkaccount/api/accounts/"
