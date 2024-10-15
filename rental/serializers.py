from rest_framework import serializers

from .models import Car, Reservation

from django.contrib.auth.models import User

from datetime import timedelta

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



    def validate(self, data):
        car = data['car']
        start_date = data['start_date']
        end_date = data['end_date']
        
        # Search for reservations to the same car
        overlapping_reservations = Reservation.objects.filter(
            car=car,
            end_date__gte=start_date  # Check that other reservations are finished or on the new start date
        )

        # If there are previous reservations, the reservation is prohibited
        if overlapping_reservations.exists():
            # Get the last reservation for the same car
            last_reservation = overlapping_reservations.order_by('-end_date').first()

            # Check that the new reservation begins after the end of the last reservation
            if start_date <= last_reservation.end_date:
                raise serializers.ValidationError({
                    'start_date': f"This car is already reserved until {last_reservation.end_date}. You can start your reservation from {last_reservation.end_date + timedelta(days=1)}."
                })

       # If everything is fine, the data is passed
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']