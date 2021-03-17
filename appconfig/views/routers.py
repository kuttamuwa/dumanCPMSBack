from rest_framework import routers

from appconfig.views.api import DomainsAPI, SubtypesAPI

router = routers.DefaultRouter()

router.register(r'domains/', DomainsAPI)
router.register(r'subtypes/', SubtypesAPI)
# router.register(r'davatar/', AvatarAPI)
