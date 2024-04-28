from django.contrib import admin
from hotel.models import buyer, hotel, category, Review

# Register your models here.


admin.site.register(buyer)
admin.site.register(hotel)
admin.site.register(category)
admin.site.register(Review)
