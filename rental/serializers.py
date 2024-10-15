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
    total_price = serializers.SerializerMethodField()  # Add total price field to the response
    class Meta:
        model = Reservation
        fields = ['id', 'customer', 'car_name', 'car', 'start_date', 'end_date','total_price']

    def get_total_price(self, obj):
        # Calculate the total days of the reservation
        num_days = (obj.end_date - obj.start_date).days
        # Multiply the number of days by the rent_per_day of the car
        total_price = num_days * obj.car.rent_per_day
        return total_price


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']