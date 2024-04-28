from django.db import models
from hotel.models import hotel, buyer

# Create your models here.
hotel_status = [("Booked", "booked"), ("Pre Booked", "pre booked")]


class hotel_booked(models.Model):
    buyer = models.ForeignKey(buyer, on_delete=models.CASCADE)
    hotel = models.ForeignKey(hotel, on_delete=models.CASCADE)
    booked_status = models.CharField(choices=hotel_status, max_length=20)
    check_in_time = models.DateTimeField()
    cancel = models.BooleanField(default=False)

    def __str__(self):
        return f"Hotel : {self.hotel.name} , Buyer : {self.buyer.first_name}"
