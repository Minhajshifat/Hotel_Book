from django.contrib import admin
from hotel.models import buyer, hotel, category, Review


# Register your models here.
class BuyerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "image"]

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name


admin.site.register(buyer, BuyerAdmin)
admin.site.register(hotel)
admin.site.register(category)
admin.site.register(Review)
