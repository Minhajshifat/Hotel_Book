from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token

# for sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect
from rest_framework import filters, pagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.permissions import BasePermission


class CategoryForSpecificHotel(filters.BaseFilterBackend):
    def filter_queryset(self, request, query_set, view):
        hotel_id = request.query_params.get("hotel_id")
        if hotel_id:
            return query_set.filter(hotel=hotel_id)
        return query_set


class CategoryViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = models.category.objects.all()
    serializer_class = serializers.categorySerializer
    filter_backends = [CategoryForSpecificHotel]


class HotelPagination(pagination.PageNumberPagination):
    page_size = 9
    page_size_query_param = page_size
    max_page_size = 100


class HotelViewset(viewsets.ModelViewSet):
    queryset = models.hotel.objects.all()
    serializer_class = serializers.hotelSerializer
    filter_backends = [filters.SearchFilter]
    pagination_class = HotelPagination
    search_fields = [
        "id",
        "name",
        "title",
        "address__address",
    ]


class BuyerViewset(viewsets.ModelViewSet):
    queryset = models.buyer.objects.all()
    serializer_class = serializers.buyerSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get("user_id")
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset


class ReviewViewset(viewsets.ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "reviewer__id",
        "hotel__id",
    ]


class UserRegistrationApiView(APIView):
    serializer_class = serializers.RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            print(user)
            token = default_token_generator.make_token(user)
            print("token ", token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print("uid ", uid)
            confirm_link = (
                f"https://hotel-book-v78k.onrender.com/hotel/active/{uid}/{token}"
            )
            email_subject = "Confirm Your Email"
            email_body = render_to_string(
                "confirm_email.html", {"confirm_link": confirm_link}
            )

            email = EmailMultiAlternatives(email_subject, "", to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response("Check your mail for confirmation")
        return Response(serializer.errors)


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except User.DoesNotExist:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("login")
    else:
        return redirect("register")


class UserLoginApiView(APIView):
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = authenticate(username=username, password=password)

            if user:
                token, _ = Token.objects.get_or_create(user=user)
                print(token)
                login(request, user)
                return Response({"token": token.key, "user_id": user.id})
            else:
                return Response({"error": "Invalid Credential"})
        return Response(serializer.errors)


class UserLogoutView(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return redirect("login")
