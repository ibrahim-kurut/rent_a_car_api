from django.db import models

from django.contrib.auth.models import User


class Car(models.Model):

    GEAR_CHOICES = [
        ('A', 'Automatic'),
        ('M', 'Manual'),
    ]

    plate_number = models.CharField(max_length=10, unique=True)  
    brand = models.CharField(max_length=50)  
    model = models.CharField(max_length=50)  
    year = models.SmallIntegerField()
    gear = models.CharField(max_length=1, choices=GEAR_CHOICES, default='A')  
    rent_per_day = models.IntegerField()  
    availability = models.BooleanField(default=True)  

    def __str__(self):
        return f"{self.brand} {self.model} - {self.plate_number}"



class Reservation(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)  
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField() 
    end_date = models.DateField()  

    def __str__(self):
        return f"Reservation by {self.customer.username} for {self.car.plate_number}"

    class Meta:
        # Preventing the recurrence of the same car on the same date
        unique_together = ('car', 'start_date', 'end_date')

