from Application.views import CustomerUserViewSet
from rest_framework import routers

router=routers.DefaultRouter()
router.register('customuser',CustomerUserViewSet)