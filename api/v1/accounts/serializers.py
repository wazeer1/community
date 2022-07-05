from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import Profile




class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    phone = serializers.CharField()
    name = serializers.CharField()
    ign = serializers.CharField()
    country = serializers.CharField()
    ig_id = serializers.CharField()

class OtpSerializer(serializers.Serializer):
    phone = serializers.CharField()
    country = serializers.CharField()

class VerifySerializer(serializers.Serializer):
    phone = serializers.CharField()
    country = serializers.CharField()
    otp = serializers.CharField()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()