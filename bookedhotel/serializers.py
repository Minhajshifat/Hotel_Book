from rest_framework import serializers
from . import models


class BookedSerializer(serializers.ModelSerializer):
    buyer = serializers.StringRelatedField(many=False)
    hotel = serializers.StringRelatedField(many=False)

    class Meta:
        model = models.hotel_booked
        fields = "__all__"
