from rest_framework import serializers
from . import models


class BookedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.hotel_booked
        fields = "__all__"
