from rest_framework import routers

from checkaccount.views.api import CheckAccountAPI, SectorsAPI, SysPersonnelAPI
from checkaccount.views.api import CitiesAPI, DistrictAPI

router = routers.DefaultRouter(trailing_slash=True)

router.register(r'accounts', CheckAccountAPI)
router.register(r'sectors', SectorsAPI)
router.register(r'syspersonnels', SysPersonnelAPI)
router.register(r'cities', CitiesAPI)
router.register(r'district', DistrictAPI)
