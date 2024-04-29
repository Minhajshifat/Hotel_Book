from rest_framework import serializers
from . import models
from django.contrib.auth.models import User


class hotelSerializer(serializers.ModelSerializer):
    address = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.hotel
        fields = "__all__"


class buyerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)

    class Meta:
        model = models.buyer
        fields = "__all__"


class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.category
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField(many=False)

    class Meta:
        model = models.Review
        fields = "__all__"


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "confirm_password",
        ]

    def save(self):
        username = self.validated_data["username"]
        first_name = self.validated_data["first_name"]
        last_name = self.validated_data["last_name"]
        email = self.validated_data["email"]
        password = self.validated_data["password"]
        password2 = self.validated_data["confirm_password"]

        if password != password2:
            raise serializers.ValidationError({"error": "Password Doesn't Mactched"})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "Email Already exists"})
        account = User(
            username=username, email=email, first_name=first_name, last_name=last_name
        )
        print(account)
        account.set_password(password)
        account.is_active = False
        account.save()
        return account


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
