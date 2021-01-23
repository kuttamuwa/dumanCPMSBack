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
