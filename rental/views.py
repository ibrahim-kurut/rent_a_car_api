
from rest_framework import viewsets

from rest_framework import status

from .models import Car, Reservation

from .serializers import CarSerializer, ReservationSerializer, UserSerializer

from django.contrib.auth.models import User

from rest_framework.decorators import action

from rest_framework.response import Response

from django.db.models import Q

from datetime import datetime

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def get_queryset(self):
        # Retrieve the start_date and end_date from the request query parameters
        start_date_str = self.request.query_params.get('start_date')
        end_date_str = self.request.query_params.get('end_date')

        if start_date_str and end_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                # Query to exclude cars that are reserved within the given date range
                reserved_cars = Reservation.objects.filter(
                    Q(start_date__lte=end_date) & Q(end_date__gte=start_date)
                ).values_list('car_id', flat=True)

                # Return cars that are available and not in the reserved cars list
                return Car.objects.filter(availability=True).exclude(id__in=reserved_cars)
            except ValueError:
                # If date format is invalid, return an empty queryset or handle accordingly
                return Car.objects.none()

        # If no dates are provided, return all available cars
        return Car.objects.filter(availability=True)



class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
        # Add the username automatically to reserve
        serializer.save(customer=self.request.user)


