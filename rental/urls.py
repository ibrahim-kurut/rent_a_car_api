# rental/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarViewSet, ReservationViewSet

router = DefaultRouter()
router.register('cars', CarViewSet)
router.register('reservations', ReservationViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
