from rest_framework import serializers

from .models import Car, Reservation

from django.contrib.auth.models import User


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'plate_number', 'brand', 'model', 'year', 'gear', 'rent_per_day', 'availability']


class ReservationSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField(source='customer.username')  # View the username instead of the ID
    car_name = serializers.ReadOnlyField(source='car.brand')  # Add a the name car to response
    class Meta:
        model = Reservation
        fields = ['id', 'customer', 'car_name', 'car', 'start_date', 'end_date']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']