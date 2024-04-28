from django.contrib import admin
from . import models
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Register your models here.


class BookedAdmin(admin.ModelAdmin):
    list_display = [
        "buyer_name",
        "hotel_name",
        "booked_status",
        "check_in_time",
        "cancel",
    ]

    def buyer_name(self, obj):
        return obj.buyer.client.username

    def hotel_name(self, obj):
        return obj.hotel.name

    def save_model(self, request, obj, form, change):
        obj.save()
        email_subject = "You Booked a hotel"
        email_body = render_to_string(
            "admin_email.html", {"buyer": obj.buyer.client, "hotel": obj.hotel}
        )
        email = EmailMultiAlternatives(email_subject, "", to=[obj.buyer.client.email])
        email.attach_alternative(email_body, "text/html")
        email.send()


admin.site.register(models.hotel_booked, BookedAdmin)
