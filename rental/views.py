
from rest_framework import viewsets

from rest_framework import status

from .models import Car, Reservation

from .serializers import CarSerializer, ReservationSerializer, UserSerializer

from django.contrib.auth.models import User

from rest_framework.decorators import action

from rest_framework.response import Response

from django.db.models import Q


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer



class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
        # Add the username automatically to reserve
        serializer.save(customer=self.request.user)


