from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers


class BookedViewSet(viewsets.ModelViewSet):
    queryset = models.hotel_booked.objects.all()
    serializer_class = serializers.BookedSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        buyer_id = self.request.query_params.get("buyer_id")
        if buyer_id:
            queryset = queryset.filter(buyer_id=buyer_id)
        return queryset


# Create your views here.
