from django.db import models
from django.contrib.auth.models import User


class category(models.Model):
    address = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100)

    def __str__(self) -> str:
        return self.address


# Create your models here.
class hotel(models.Model):
    image = models.ImageField(upload_to="hotal/images/")
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=100)
    rooms = models.IntegerField()
    description = models.TextField()
    price = models.IntegerField()
    address = models.ManyToManyField(category)

    def __str__(self) -> str:
        return self.name


class buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to="buyer/images", blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"


STAR_CHOICES = [
    ("⭐", "⭐"),
    ("⭐⭐", "⭐⭐"),
    ("⭐⭐⭐", "⭐⭐⭐"),
    ("⭐⭐⭐⭐", "⭐⭐⭐⭐"),
    ("⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"),
]


class Review(models.Model):
    reviewer = models.ForeignKey(buyer, on_delete=models.CASCADE)
    hotel = models.ForeignKey(hotel, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    rating = models.CharField(choices=STAR_CHOICES, max_length=10)

    def __str__(self):
        return f"Buyer : {self.reviewer.user.first_name} ; hotel {self.hotel.name}"
