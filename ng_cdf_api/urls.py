from django.urls import path, include
from rest_framework import routers
from .views import (
    AuthViewset,
    NGCDFViewset,
    BursaryViewset
)


router = routers.DefaultRouter(trailing_slash=False)
router.register('api/auth', AuthViewset, basename='auth')
router.register('api/ng_cdf', NGCDFViewset, basename='ng_cdf')
router.register('api/bursary', BursaryViewset, basename='bursary')


urlpatterns = [
    path(r'', include(router.urls)),
]